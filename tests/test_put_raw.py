from pathlib import Path
from typing import Any

import pytest

from dbt_test_mmm.config import SnowflakeConfig
from dbt_test_mmm.put_raw import (
    DATASETS,
    STAGE_NAME,
    build_put_sql,
    infer_dataset_from_file,
    put_files,
    select_ranking_files,
    selected_datasets,
)


def _test_config() -> SnowflakeConfig:
    return SnowflakeConfig(
        account="test-account",
        user="test-user",
        role="TEST_ROLE",
        warehouse="TEST_WH",
        database="TEST_DB",
        raw_schema="RAW",
        private_key_path=Path("dummy.p8"),
    )


def test_selected_datasets_returns_all_in_stable_order():
    assert [dataset.name for dataset in selected_datasets("all")] == [
        "player_ranking",
        "guild_ranking",
    ]


def test_infer_dataset_from_file_uses_parent_directory():
    assert infer_dataset_from_file(Path("data/player_ranking/2026-03-18_1.json")).name == (
        "player_ranking"
    )
    assert infer_dataset_from_file(Path("data/guild_ranking/2026-03-18_1.json")).name == (
        "guild_ranking"
    )


def test_infer_dataset_from_file_rejects_unknown_directory():
    with pytest.raises(ValueError, match="Cannot infer dataset"):
        infer_dataset_from_file(Path("data/unknown/2026-03-18_1.json"))


def test_select_ranking_files_returns_newest_names_first(tmp_path):
    old_file = tmp_path / "2026-03-17_1.json"
    new_file = tmp_path / "2026-03-18_1.json"
    old_file.write_text("{}", encoding="utf-8")
    new_file.write_text("{}", encoding="utf-8")

    assert select_ranking_files(tmp_path) == [new_file, old_file]


def test_select_ranking_files_applies_limit(tmp_path):
    for name in ["2026-03-16_1.json", "2026-03-17_1.json", "2026-03-18_1.json"]:
        (tmp_path / name).write_text("{}", encoding="utf-8")

    assert select_ranking_files(tmp_path, limit=2) == [
        tmp_path / "2026-03-18_1.json",
        tmp_path / "2026-03-17_1.json",
    ]


def test_select_ranking_files_rejects_non_positive_limit(tmp_path):
    with pytest.raises(ValueError, match="limit"):
        select_ranking_files(tmp_path, limit=0)


def test_build_put_sql_uses_single_stage_and_dataset_path(tmp_path):
    file_path = tmp_path / "2026-03-18_1.json"
    file_path.write_text("not read by loader", encoding="utf-8")

    put_sql = build_put_sql(file_path, DATASETS["guild_ranking"])

    assert f"@{STAGE_NAME}/data/guild_ranking" in put_sql
    assert f"file://{file_path.resolve()}" in put_sql
    assert "auto_compress=false" in put_sql
    assert "overwrite=false" in put_sql


def test_put_files_executes_put_without_reading_json(monkeypatch, tmp_path):
    file_path = tmp_path / "2026-03-18_1.json"
    file_path.write_text("not json", encoding="utf-8")

    class FakeCursor:
        def __init__(self) -> None:
            self.executed: list[str] = []

        def __enter__(self) -> "FakeCursor":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def execute(self, sql: str) -> None:
            self.executed.append(sql)

    class FakeConnection:
        def __init__(self) -> None:
            self.cursor_instance = FakeCursor()

        def __enter__(self) -> "FakeConnection":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def cursor(self) -> FakeCursor:
            return self.cursor_instance

    fake_connection = FakeConnection()

    def fake_connect(**kwargs: Any) -> FakeConnection:
        return fake_connection

    monkeypatch.setattr("dbt_test_mmm.put_raw.snowflake.connector.connect", fake_connect)

    put_count = put_files(_test_config(), [file_path], DATASETS["player_ranking"])

    assert put_count == 1
    assert len(fake_connection.cursor_instance.executed) == 1
    assert "insert into" not in fake_connection.cursor_instance.executed[0].lower()
    assert f"@{STAGE_NAME}/data/player_ranking" in fake_connection.cursor_instance.executed[0]
