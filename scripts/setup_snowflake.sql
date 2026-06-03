use warehouse dbt_test_mmm_wh;
use role dbt_test_mmm_role;
use database dbt_test_mmm_db;

create schema if not exists raw;
create schema if not exists staging;
create schema if not exists marts;

create table if not exists raw.raw_player_ranking_json (
    loaded_at timestamp_ntz not null,
    collected_at timestamp_ntz not null,
    source_file string not null,
    raw_payload variant not null
);
