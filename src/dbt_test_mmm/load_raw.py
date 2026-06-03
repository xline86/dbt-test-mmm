from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

import snowflake.connector

from dbt_test_mmm.config import SnowflakeConfig

DEFAULT_DATA_DIR = Path("data/player_ranking")


def select_ranking_files(
    data_dir: Path = DEFAULT_DATA_DIR,
    *,
    file_path: Path | None = None,
    limit: int | None = None,
) -> list[Path]:
    if file_path is not None:
        files = [file_path]
    else:
        files = sorted(data_dir.glob("*.json"), reverse=True)

    if limit is not None:
        if limit < 1:
            raise ValueError("limit must be greater than zero")
        files = files[:limit]

    return files


def read_payload(path: Path) -> tuple[str, str]:
    payload_text = path.read_text(encoding="utf-8")
    payload = json.loads(payload_text)
    collected_at = payload.get("datetime")
    if not isinstance(collected_at, str):
        raise ValueError(f"{path} does not contain a string datetime field")
    datetime.fromisoformat(collected_at)
    return collected_at, payload_text


def build_insert_sql(config: SnowflakeConfig) -> str:
    return f"""
        insert into {config.raw_table}
            (loaded_at, collected_at, source_file, raw_payload)
        select
            current_timestamp()::timestamp_ntz,
            to_timestamp_ntz(%s),
            %s,
            parse_json(%s)
    """


def load_files(config: SnowflakeConfig, files: Sequence[Path]) -> int:
    insert_sql = build_insert_sql(config)

    loaded_count = 0
    with snowflake.connector.connect(**config.connection_kwargs()) as connection:
        with connection.cursor() as cursor:
            for file_path in files:
                collected_at, payload_text = read_payload(file_path)
                cursor.execute(insert_sql, (collected_at, file_path.name, payload_text))
                loaded_count += 1
        connection.commit()

    return loaded_count
