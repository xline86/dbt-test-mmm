# アーキテクチャ

このプロジェクトは、ローカル JSON を Snowflake RAW にロードし、dbt で staging と marts を作る最小構成です。

```
data/player_ranking/*.json
  ↓ Python loader
DBT_TEST_MMM_DB.RAW.RAW_PLAYER_RANKING_JSON
  ↓ dbt staging view
DBT_TEST_MMM_DB.STAGING.stg_player_ranking
  ↓ dbt mart table
DBT_TEST_MMM_DB.MARTS.mart_top_players_latest
```

## RAW

RAW テーブルは JSON を再処理できるように、加工を最小限にします。

| column         | type            | note                       |
| -------------- | --------------- | -------------------------- |
| `loaded_at`    | `timestamp_ntz` | Snowflake にロードした時刻 |
| `collected_at` | `timestamp_ntz` | JSON の `datetime`         |
| `source_file`  | `string`        | 元ファイル名               |
| `raw_payload`  | `variant`       | JSON 全体                  |

## staging

`stg_player_ranking` は `rankings` 配下のランキング配列を縦持ちに展開します。

主なカラム:

- `collected_at`
- `world_id`
- `ranking_type`
- `rank_position`
- `player_id`
- `player_name`
- `score_value`

`score_value` はランキング種別に応じて `bp`, `rank`, `quest_id`, `tower_id` の値を入れます。

## marts

`mart_top_players_latest` は最新 `collected_at` のランキング行だけを保持する分析用テーブルです。最小構成では intermediate 層は作らず、差分分析や player dimension は後続で追加します。

dbt の schema naming は `dbt/macros/generate_schema_name.sql` で上書きし、`STAGING` と `MARTS` に直接モデルを作成します。
