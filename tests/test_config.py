from pathlib import Path

from dbt_test_mmm.config import load_config


def test_load_config_builds_key_pair_connection_kwargs(monkeypatch):
    monkeypatch.setenv("SNOWFLAKE_ACCOUNT", "test-account")
    monkeypatch.setenv("SNOWFLAKE_USER", "test-user")
    monkeypatch.setenv("SNOWFLAKE_ROLE", "TEST_ROLE")
    monkeypatch.setenv("SNOWFLAKE_WAREHOUSE", "TEST_WH")
    monkeypatch.setenv("SNOWFLAKE_DATABASE", "TEST_DB")
    monkeypatch.setenv("SNOWFLAKE_RAW_SCHEMA", "RAW")
    monkeypatch.setenv("SNOWFLAKE_PRIVATE_KEY_PATH", "~/keys/snowflake.p8")
    monkeypatch.setenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE", "secret")

    config = load_config()

    assert config.raw_table == "TEST_DB.RAW.RAW_PLAYER_RANKING_JSON"
    assert config.connection_kwargs() == {
        "account": "test-account",
        "user": "test-user",
        "role": "TEST_ROLE",
        "warehouse": "TEST_WH",
        "database": "TEST_DB",
        "schema": "RAW",
        "private_key_file": str(Path("~/keys/snowflake.p8").expanduser()),
        "private_key_file_pwd": "secret",
    }
