{{
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key=['source_file', 'world_id', 'ranking_type', 'guild_id']
    )
}}

select
    world_id,
    guild_id,
    guild_name,
    ranking_type,
    collected_at,
    rank_position,
    score_value,
    source_file
from {{ ref('stg_guild_ranking_all') }}

{% if is_incremental() %}
where source_file not in (
    select distinct source_file from {{ this }}
)
{% endif %}
