# dbt-test

Snowflake 無料トライアルと dbt Core で、ゲームの `player_ranking` JSON を RAW にロードし、dbt でランキング分析用の最小 mart を作る学習用プロジェクトです。

データ構造の詳細は [docs/player_rankingデータ構造.md](docs/player_rankingデータ構造.md) を参照してください。`data/` は git 管理しません。

## セットアップ

```sh
uv sync
cp .env.example .env
cp config/profiles.yml.example config/profiles.yml
```

`.env` には Snowflake の key-pair 認証情報を設定します。
`config/profiles.yml` に編集の必要はありません

## 実行順序

```sh
# Snowflake オブジェクト作成
make setup

# 最新 JSON 1 件を RAW にロード
make load

# dbt 接続確認
make dbt-debug

# staging と mart の作成、dbt tests の実行
make dbt-build

# Python lint、型チェック、pytest
make check
```

`make load` はデフォルトで最新 1 件のみロードします。全件ロードする場合は次のように実行します。

```sh
make load LOAD_ARGS=
```

## 構成

- `src/dbt_test_mmm/`: Snowflake RAW ロード用 Python CLI
- `dbt/`: dbt project、staging、marts、dbt tests
- `scripts/`: Snowflake セットアップ SQL
- `config/`: dbt profiles のサンプル
- `docs/`: アーキテクチャと運用手順

詳細は [docs/architecture.md](docs/architecture.md) と [docs/operation.md](docs/operation.md) を参照してください。
