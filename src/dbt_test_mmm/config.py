from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class SnowflakeConfig:
    account: str
    user: str
    role: str
    warehouse: str
    database: str
    raw_schema: str
    private_key_path: Path
    private_key_passphrase: str | None = None

    @property
    def raw_table(self) -> str:
        return f"{self.database}.{self.raw_schema}.RAW_PLAYER_RANKING_JSON"

    def connection_kwargs(self) -> dict[str, object]:
        kwargs: dict[str, object] = {
            "account": self.account,
            "user": self.user,
            "role": self.role,
            "warehouse": self.warehouse,
            "database": self.database,
            "schema": self.raw_schema,
            "private_key_file": str(self.private_key_path),
        }
        if self.private_key_passphrase:
            kwargs["private_key_file_pwd"] = self.private_key_passphrase
        return kwargs


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_config(env_file: Path | None = None) -> SnowflakeConfig:
    if env_file is None:
        load_dotenv()
    else:
        load_dotenv(env_file)

    return SnowflakeConfig(
        account=_required_env("SNOWFLAKE_ACCOUNT"),
        user=_required_env("SNOWFLAKE_USER"),
        role=os.getenv("SNOWFLAKE_ROLE", "DBT_TEST_MMM_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE", "DBT_TEST_MMM_WH"),
        database=os.getenv("SNOWFLAKE_DATABASE", "DBT_TEST_MMM_DB"),
        raw_schema=os.getenv("SNOWFLAKE_RAW_SCHEMA", "RAW"),
        private_key_path=Path(_required_env("SNOWFLAKE_PRIVATE_KEY_PATH")).expanduser(),
        private_key_passphrase=os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE") or None,
    )
