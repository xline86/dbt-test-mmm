# 運用手順

## 1. 依存関係

```sh
uv sync
```

## 2. Snowflake 接続設定

```sh
cp .env.example .env
cp config/profiles.yml.example config/profiles.yml
```

`.env` に key-pair 認証情報を設定します。

```sh
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_ROLE=DBT_TEST_MMM_ROLE
SNOWFLAKE_WAREHOUSE=DBT_TEST_MMM_WH
SNOWFLAKE_DATABASE=DBT_TEST_MMM_DB
SNOWFLAKE_RAW_SCHEMA=RAW
SNOWFLAKE_PRIVATE_KEY_PATH=/home/you/.ssh/snowflake_rsa_key.p8
SNOWFLAKE_PRIVATE_KEY_PASSPHRASE=
SNOWFLAKE_PUBLIC_KEY_PATH=/home/you/.ssh/snowflake_rsa_key.pub
SNOWFLAKE_ADMIN_CONNECTION=CONN_ADMIN
SNOWFLAKE_DEV_CONNECTION=CONN_MMM
```

## 3. Snowflake オブジェクト作成

Snowflake のセットアップは 2 段階に分けます。

- `make setup-admin`: `ACCOUNTADMIN` を持つ接続で、role / warehouse / database / developer user / grants を作成する
- `make setup`: 開発者ユーザー `mmm` の接続で、`raw` / `staging` / `marts` schema と RAW table を作成する

`setup_snowflake_by_admin.sql` は公開鍵を直書きしません。`make setup-admin` は `.env` の `SNOWFLAKE_PUBLIC_KEY_PATH` から mmm ユーザー用の公開鍵ファイルを読み、SQL テンプレート変数 `dbt_user_rsa_public_key` に渡します。

```sh
make setup-admin
make setup
```

`CONN_ADMIN` と `CONN_MMM` の両方が Snowflake CLI に設定済みなら、まとめて実行できます。

```sh
make setup-all
```

Snowflake CLI の接続名を変更する場合は `.env` か実行時変数で指定します。

```sh
make setup-admin SNOWFLAKE_ADMIN_CONNECTION=CONN_ADMIN
make setup SNOWFLAKE_DEV_CONNECTION=CONN_MMM
```

公開鍵ファイルを明示する場合:

```sh
make setup-admin SNOWFLAKE_PUBLIC_KEY_PATH=/home/you/.ssh/snowflake_rsa_key.pub
```

作成される Snowflake オブジェクト:
- `scripts/setup_snowflake_by_admin.sql`: `dbt_test_mmm_role` / `dbt_test_mmm_wh` / `dbt_test_mmm_db` / user `mmm`
- `scripts/setup_snowflake.sql`: `raw` / `staging` / `marts` schema と `raw.raw_player_ranking_json`

管理者側では database ownership を `dbt_test_mmm_role` へ付与します。開発者側で作成した schema/table も同じロールが所有します。

## 4. RAW ロード

最新 1 件だけロードします。

```sh
make load
```

ファイルを指定してロードします。

```sh
uv run dbt-test load-raw --file data/player_ranking/2026-03-18_1.json
```

全件ロードします。

```sh
make load LOAD_ARGS=
```

## 5. dbt 実行

```sh
make dbt-debug
make dbt-build
```

`config/profiles.yml` はローカル用設定ファイルです。秘密情報は `.env` に置き、git 管理しないでください。

## 6. チェック

```sh
make check
```

実行内容:

- `ruff check src tests`
- `pyright`
- `pytest`

## 7. Snowflake Git Repository

git連携したワークスペースの作成はsnowsight上でのUI操作によって行ったためsqlは残していません

方法
1. Gitリポジトリからワークスペースを作成 を押下
2. リポジトリURLとワークスペース名を決める
3. API統合を指定する。存在しない場合は作成する
4. 「構成」ボタンを押下してgithubのサイトから認証を行う
5. 「作成」でワークスペースを作成する
