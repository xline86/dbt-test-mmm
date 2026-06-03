with raw_rankings as (
    select
        collected_at,
        source_file,
        raw_payload:data:world_id::number as world_id,
        raw_payload:data:rankings as rankings
    from {{ source('raw', 'raw_guild_ranking_json') }}
),

bp as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'bp' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as guild_id,
        ranking.value:name::string as guild_name,
        ranking.value:bp::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:bp) as ranking
),

level as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'level' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as guild_id,
        ranking.value:name::string as guild_name,
        ranking.value:level::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:level) as ranking
),

stock as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'stock' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as guild_id,
        ranking.value:name::string as guild_name,
        ranking.value:stock::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:stock) as ranking
)

select * from bp
union all
select * from level
union all
select * from stock
