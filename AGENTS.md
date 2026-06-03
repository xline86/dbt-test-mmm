## プロジェクト

Snowflake と dbt Core で、`player_ranking` JSON を RAW にロードし、staging と mart を作る学習用プロジェクトです。

RAW の日時型は `TIMESTAMP_NTZ` を使います。`TIMESTAMP_LTZ` は使いません。

## データ

`data/` には 1200 件以上の大きな JSON があります。JSON 本体は直接読まないでください。

ファイル名だけ確認する場合は次を使います。

```sh
ls data/player_ranking | sort -r | head -n 5
```

データ構造は [docs/player_rankingデータ構造.md](docs/player_rankingデータ構造.md) を参照します。

## チェック

通常の確認は次を使います。

```sh
make check
```

`make check` は `ruff check src tests`、`pyright`、`pytest` を実行します。

- コードを整形する場合は次を使う。
```sh
uv run ruff format .
```

- lintの自動修正が必要な場合は次を使う。
```sh
uv run ruff check . --fix
```
