from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import snowflake.connector

from dbt_test_mmm.config import SnowflakeConfig

DatasetName = Literal["player_ranking", "guild_ranking"]
DatasetSelection = Literal["player_ranking", "guild_ranking", "all"]

DEFAULT_DATA_ROOT = Path("data")
STAGE_NAME = "raw.mmm_ranking_stage"


@dataclass(frozen=True)
class RankingDataset:
    name: DatasetName
    data_dir: Path

    @property
    def stage_path(self) -> str:
        return f"data/{self.name}"


DATASETS: dict[DatasetName, RankingDataset] = {
    "player_ranking": RankingDataset("player_ranking", DEFAULT_DATA_ROOT / "player_ranking"),
    "guild_ranking": RankingDataset("guild_ranking", DEFAULT_DATA_ROOT / "guild_ranking"),
}


def selected_datasets(selection: DatasetSelection) -> list[RankingDataset]:
    if selection == "all":
        return list(DATASETS.values())
    return [DATASETS[selection]]


def infer_dataset_from_file(file_path: Path) -> RankingDataset:
    if file_path.parent.name == "player_ranking":
        return DATASETS["player_ranking"]
    if file_path.parent.name == "guild_ranking":
        return DATASETS["guild_ranking"]

    valid_dirs = ", ".join(dataset.name for dataset in DATASETS.values())
    raise ValueError(f"Cannot infer dataset from {file_path}; parent directory must be {valid_dirs}")


def select_ranking_files(
    data_dir: Path,
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


def build_put_sql(file_path: Path, dataset: RankingDataset) -> str:
    return (
        f"put 'file://{file_path.resolve()}' "
        f"@{STAGE_NAME}/{dataset.stage_path} "
        "auto_compress=false overwrite=false"
    )


def put_files(config: SnowflakeConfig, files: Sequence[Path], dataset: RankingDataset) -> int:
    put_count = 0
    with snowflake.connector.connect(**config.connection_kwargs()) as connection:
        with connection.cursor() as cursor:
            for file_path in files:
                cursor.execute(build_put_sql(file_path, dataset))
                put_count += 1

    return put_count
