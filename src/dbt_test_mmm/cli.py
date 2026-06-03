from __future__ import annotations

from pathlib import Path

import click

from dbt_test_mmm.config import load_config
from dbt_test_mmm.load_raw import DEFAULT_DATA_DIR, load_files, select_ranking_files


@click.group()
def main() -> None:
    """Command line helpers for the dbt_test_mmm ELT project."""


@main.command("load-raw")
@click.option(
    "--data-dir",
    type=click.Path(path_type=Path, file_okay=False, dir_okay=True),
    default=DEFAULT_DATA_DIR,
    show_default=True,
    help="Directory containing player_ranking JSON files.",
)
@click.option(
    "--file",
    "file_path",
    type=click.Path(path_type=Path, file_okay=True, dir_okay=False),
    default=None,
    help="Load a single JSON file instead of scanning the data directory.",
)
@click.option("--limit", type=int, default=None, help="Limit the number of newest files to load.")
@click.option(
    "--env-file",
    type=click.Path(path_type=Path, file_okay=True, dir_okay=False),
    default=None,
    help="Optional .env file path.",
)
def load_raw(
    data_dir: Path, file_path: Path | None, limit: int | None, env_file: Path | None
) -> None:
    config = load_config(env_file)
    files = select_ranking_files(data_dir=data_dir, file_path=file_path, limit=limit)
    if not files:
        raise click.ClickException(f"No JSON files found in {data_dir}")

    loaded_count = load_files(config, files)
    click.echo(f"Loaded {loaded_count} file(s) into {config.raw_table}")
