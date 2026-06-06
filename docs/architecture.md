# アーキテクチャ

このプロジェクトは、ローカル JSON を Snowflake RAW にロードし、dbt で staging と marts を作る最小構成です。

```
data/player_ranking/*.json, data/guild_ranking/*.json
  ↓ Python PUT / Snowflake CLI PUT
DBT_TEST_MMM_DB.RAW.MMM_RANKING_STAGE
  ↓ COPY INTO
DBT_TEST_MMM_DB.RAW.RAW_PLAYER_RANKING_JSON
DBT_TEST_MMM_DB.RAW.RAW_GUILD_RANKING_JSON
  ↓ dbt staging view
DBT_TEST_MMM_DB.STAGING.stg_player_ranking
DBT_TEST_MMM_DB.STAGING.stg_guild_ranking
DBT_TEST_MMM_DB.STAGING.stg_player_info
DBT_TEST_MMM_DB.STAGING.stg_guild_info
DBT_TEST_MMM_DB.STAGING.stg_player_ranking_all
DBT_TEST_MMM_DB.STAGING.stg_guild_ranking_all
  ↓ dbt mart table
DBT_TEST_MMM_DB.MARTS.mart_player_ranking_latest
DBT_TEST_MMM_DB.MARTS.mart_guild_ranking_latest
DBT_TEST_MMM_DB.MARTS.mart_player_ranking_history
DBT_TEST_MMM_DB.MARTS.mart_guild_ranking_history
```

## RAW

RAW テーブルは JSON を再処理できるように、加工を最小限にします。内部 stage は `raw.mmm_ranking_stage` を 1 つだけ使い、`data/player_ranking/` と `data/guild_ranking/` の path で分けます。

| column         | type            | note                       |
| -------------- | --------------- | -------------------------- |
| `loaded_at`    | `timestamp_ntz` | Snowflake にロードした時刻 |
| `collected_at` | `timestamp_ntz` | JSON の `datetime`         |
| `source_file`  | `string`        | 元ファイル名               |
| `raw_payload`  | `variant`       | JSON 全体                  |

## staging

`stg_player_ranking` と `stg_guild_ranking` は `rankings` 配下のランキング配列を縦持ちに展開します。

RAW に同じ日付のファイルが複数ある場合、`stg_player_ranking` / `stg_guild_ranking` / `stg_player_info` / `stg_guild_info` ではファイル名末尾のサフィックスが最大のファイルだけを使います。例えば `2025-02-20_1.json` と `2025-02-20_2.json` がある場合、`_2` を代表データとして扱います。RAW には全ファイルを残します。

history mart 用には、代表ファイルに絞らない `stg_player_ranking_all` と `stg_guild_ranking_all` を使います。この 2 つは RAW の全ファイルを展開します。

主なカラム:

- `collected_at`
- `world_id`
- `ranking_type`
- `rank_position`
- `player_id` / `guild_id`
- `player_name` / `guild_name`
- `score_value`

`score_value` はランキング種別に応じて `bp`, `rank`, `quest_id`, `tower_id`, `level`, `stock` の値を入れます。

## marts

mart 層は、分析で直接使いやすい latest / profile / history / summary のテーブルを作成します。dbt の `description` は Snowflake の table / column comment として反映します。

- `mart_player_ranking_latest`: 各ワールド・ランキング種別ごとの最新プレイヤーランキング
- `mart_top_player_profile_latest`: 最新のプレイヤープロフィール。ランキングに登場したプレイヤーのみを含む
- `mart_guild_ranking_latest`: 各ワールド・ランキング種別ごとの最新ギルドランキング
- `mart_guild_profile_latest`: 最新のギルドプロフィール。同じ収集日時の player BP ランキング情報も付与する
- `mart_player_ranking_history`: プレイヤーランキング履歴
- `mart_guild_ranking_history`: ギルドランキング履歴
- `mart_world_player_ranking_summary`: ワールド単位のプレイヤーランキング概要
- `mart_world_guild_ranking_summary`: ワールド単位のギルドランキング概要

latest 系は `row_number()` で最新行を選びます。player と guild の情報を結合する場合は、同じ `world_id` と `collected_at` のデータだけを使います。

history 系の `mart_player_ranking_history` と `mart_guild_ranking_history` は dbt incremental model です。増分実行時は、mart に未登録の `source_file` だけを `stg_player_ranking_all` / `stg_guild_ranking_all` から取り込みます。作り直す場合は dbt の `--full-refresh` を使います。

dbt の schema naming は `dbt/macros/generate_schema_name.sql` で上書きし、`STAGING` と `MARTS` に直接モデルを作成します。
