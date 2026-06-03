## プロジェクト

Snowflake と dbt Core で、ranking JSON を RAW にロードし、staging と mart を作る学習用プロジェクトです。

RAW の日時型は `TIMESTAMP_NTZ` を使います。`TIMESTAMP_LTZ` は使いません。

RAW ロードは Python の PUT と SQL の COPY INTO に分けます。内部 stage は `raw.mmm_ranking_stage` を 1 つだけ使います。

## データ

`data/` には1200件以上、`data/player_ranking/` にも300件以上の大きな JSON があります。JSON 本体は直接読まないでください。

ファイル名だけ確認する場合は次を使います。

```sh
ls data/player_ranking | sort -r | head -n 5
ls data/guild_ranking | sort -r | head -n 5
```

データ構造は次を参照する
-  [docs/player_rankingデータ構造.md](docs/player_rankingデータ構造.md)
-  [docs/guild_rankingデータ構造.md](docs/guild_rankingデータ構造.md)

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
