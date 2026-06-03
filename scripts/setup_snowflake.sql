use warehouse dbt_test_mmm_wh;
use role dbt_test_mmm_role;
use database dbt_test_mmm_db;

create schema if not exists raw;
create schema if not exists staging;
create schema if not exists marts;

create file format if not exists raw.ranking_json_file_format
    type = json;

create stage if not exists raw.mmm_ranking_stage
    file_format = raw.ranking_json_file_format;

create table if not exists raw.raw_player_ranking_json (
    loaded_at timestamp_ntz not null,
    collected_at timestamp_ntz not null,
    source_file string not null,
    raw_payload variant not null
);

create table if not exists raw.raw_guild_ranking_json (
    loaded_at timestamp_ntz not null,
    collected_at timestamp_ntz not null,
    source_file string not null,
    raw_payload variant not null
);
