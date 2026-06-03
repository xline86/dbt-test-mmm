import json
from pathlib import Path

import pytest

from dbt_test_mmm.config import SnowflakeConfig
from dbt_test_mmm.load_raw import (
    build_insert_sql,
    build_loaded_source_file_sql,
    load_files,
    read_payload,
    select_ranking_files,
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


def test_build_insert_sql_uses_timestamp_ntz():
    config = _test_config()

    insert_sql = build_insert_sql(config)

    assert "current_timestamp()::timestamp_ntz" in insert_sql
    assert "to_timestamp_ntz(%s)" in insert_sql
    assert "timestamp_ltz" not in insert_sql.lower()
    assert "to_timestamp_ltz" not in insert_sql.lower()


def test_build_loaded_source_file_sql_filters_by_source_file():
    loaded_source_file_sql = build_loaded_source_file_sql(_test_config())

    assert "from TEST_DB.RAW.RAW_PLAYER_RANKING_JSON" in loaded_source_file_sql
    assert "where source_file = %s" in loaded_source_file_sql


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


def test_read_payload_returns_datetime_and_original_text(tmp_path):
    file_path = tmp_path / "ranking.json"
    payload = {"datetime": "2026-03-18T03:00:00", "datatype": "player_ranking"}
    payload_text = json.dumps(payload)
    file_path.write_text(payload_text, encoding="utf-8")

    collected_at, raw_text = read_payload(file_path)

    assert collected_at == "2026-03-18T03:00:00"
    assert raw_text == payload_text


def test_read_payload_rejects_missing_datetime(tmp_path):
    file_path = tmp_path / "ranking.json"
    file_path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="datetime"):
        read_payload(file_path)


def test_load_files_skips_already_loaded_source_file(monkeypatch, tmp_path):
    loaded_file = tmp_path / "loaded.json"
    new_file = tmp_path / "new.json"
    loaded_file.write_text("not json", encoding="utf-8")
    new_file.write_text(
        json.dumps({"datetime": "2026-03-18T03:00:00", "datatype": "player_ranking"}),
        encoding="utf-8",
    )

    class FakeCursor:
        def __init__(self):
            self.executed: list[tuple[str, tuple[object, ...]]] = []
            self._last_params: tuple[object, ...] = ()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def execute(self, sql, params):
            self.executed.append((sql, params))
            self._last_params = params

        def fetchone(self):
            if self._last_params == ("loaded.json",):
                return (1,)
            return None

    class FakeConnection:
        def __init__(self):
            self.cursor_instance = FakeCursor()
            self.committed = False

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def cursor(self):
            return self.cursor_instance

        def commit(self):
            self.committed = True

    fake_connection = FakeConnection()
    monkeypatch.setattr(
        "dbt_test_mmm.load_raw.snowflake.connector.connect",
        lambda **kwargs: fake_connection,
    )

    loaded_count = load_files(_test_config(), [loaded_file, new_file])

    assert loaded_count == 1
    assert fake_connection.committed is True
    insert_executions = [
        params
        for sql, params in fake_connection.cursor_instance.executed
        if "insert into" in sql.lower()
    ]
    assert insert_executions == [
        (
            "2026-03-18T03:00:00",
            "new.json",
            new_file.read_text(encoding="utf-8"),
        )
    ]
