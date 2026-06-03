# アーキテクチャ

このプロジェクトは、ローカル JSON を Snowflake RAW にロードし、dbt で staging と marts を作る最小構成です。

```
data/player_ranking/*.json, data/guild_ranking/*.json
  ↓ Python PUT
DBT_TEST_MMM_DB.RAW.MMM_RANKING_STAGE
  ↓ COPY INTO
DBT_TEST_MMM_DB.RAW.RAW_PLAYER_RANKING_JSON
DBT_TEST_MMM_DB.RAW.RAW_GUILD_RANKING_JSON
  ↓ dbt staging view
DBT_TEST_MMM_DB.STAGING.stg_player_ranking
DBT_TEST_MMM_DB.STAGING.stg_guild_ranking
  ↓ dbt mart table
DBT_TEST_MMM_DB.MARTS.mart_player_ranking_latest
DBT_TEST_MMM_DB.MARTS.mart_guild_ranking_latest
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

dbt の schema naming は `dbt/macros/generate_schema_name.sql` で上書きし、`STAGING` と `MARTS` に直接モデルを作成します。
