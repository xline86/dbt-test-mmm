from __future__ import annotations

from pathlib import Path

import click

from dbt_test_mmm.config import load_config
from dbt_test_mmm.put_raw import (
    DatasetSelection,
    infer_dataset_from_file,
    put_files,
    select_ranking_files,
    selected_datasets,
)


@click.group()
def main() -> None:
    """Command line helpers for the dbt_test_mmm ELT project."""


@main.command("put-raw")
@click.option(
    "--data-dir",
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True),
    default=None,
    help="Directory containing ranking JSON files. Only valid when --dataset is not all.",
)
@click.option(
    "--file",
    "file_path",
    type=click.Path(path_type=Path, file_okay=True, dir_okay=False),
    default=None,
    help="Put a single JSON file instead of scanning the data directory.",
)
@click.option("--limit", type=int, default=None, help="Limit the number of newest files to put.")
@click.option(
    "--dataset",
    type=click.Choice(["player_ranking", "guild_ranking", "all"]),
    default="all",
    show_default=True,
    help="Ranking dataset to put into the internal stage.",
)
@click.option(
    "--env-file",
    type=click.Path(path_type=Path, file_okay=True, dir_okay=False),
    default=None,
    help="Optional .env file path.",
)
def put_raw(
    data_dir: Path | None,
    file_path: Path | None,
    limit: int | None,
    dataset: DatasetSelection,
    env_file: Path | None,
) -> None:
    config = load_config(env_file)

    if file_path and dataset == "all":
        datasets = [infer_dataset_from_file(file_path)]
    else:
        datasets = selected_datasets(dataset)
    if data_dir is not None and len(datasets) != 1:
        raise click.ClickException("--data-dir can only be used with --dataset player_ranking or guild_ranking")

    put_count = 0
    for ranking_dataset in datasets:
        dataset_dir = data_dir or ranking_dataset.data_dir
        files = select_ranking_files(data_dir=dataset_dir, file_path=file_path, limit=limit)
        if not files:
            raise click.ClickException(f"No JSON files found in {dataset_dir}")

        put_count += put_files(config, files, ranking_dataset)

    click.echo(f"Put {put_count} file(s) into Snowflake internal stage")
