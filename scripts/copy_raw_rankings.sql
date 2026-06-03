use warehouse dbt_test_mmm_wh;
use role dbt_test_mmm_role;
use database dbt_test_mmm_db;

copy into raw.raw_player_ranking_json (
    loaded_at,
    collected_at,
    source_file,
    raw_payload
)
from (
    select
        current_timestamp()::timestamp_ntz,
        to_timestamp_ntz($1:datetime::string),
        metadata$filename,
        $1
    from @raw.mmm_ranking_stage/data/player_ranking/
)
on_error = abort_statement;

copy into raw.raw_guild_ranking_json (
    loaded_at,
    collected_at,
    source_file,
    raw_payload
)
from (
    select
        current_timestamp()::timestamp_ntz,
        to_timestamp_ntz($1:datetime::string),
        metadata$filename,
        $1
    from @raw.mmm_ranking_stage/data/guild_ranking/
)
on_error = abort_statement;
