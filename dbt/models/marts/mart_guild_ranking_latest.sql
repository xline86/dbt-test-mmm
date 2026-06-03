with ranked as (
    select
        ranking.world_id,
        ranking.ranking_type,
        ranking.rank_position,
        ranking.guild_id,
        ranking.guild_name,
        ranking.score_value,
        ranking.collected_at,
        row_number() over (
            partition by ranking.world_id, ranking.ranking_type, ranking.rank_position
            order by ranking.collected_at desc, ranking.source_file desc
        ) as row_number
    from {{ ref('stg_guild_ranking') }} as ranking
)

select
    world_id,
    ranking_type,
    rank_position,
    guild_id,
    guild_name,
    score_value,
    collected_at
from ranked
where row_number = 1
