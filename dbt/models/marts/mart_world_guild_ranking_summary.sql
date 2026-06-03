with ranked as (
    select
        ranking.world_id,
        ranking.collected_at,
        ranking.ranking_type,
        ranking.guild_id,
        ranking.guild_name,
        ranking.rank_position,
        ranking.score_value,
        row_number() over (
            partition by ranking.world_id, ranking.collected_at, ranking.ranking_type
            order by ranking.rank_position desc
        ) as bottom_row_number
    from {{ ref('stg_guild_ranking') }} as ranking
),

summary as (
    select
        world_id,
        collected_at,
        ranking_type,
        count(*) as entry_count,
        max(case when rank_position = 1 then guild_id end) as top_guild_id,
        max(case when rank_position = 1 then guild_name end) as top_guild_name,
        max(case when rank_position = 1 then score_value end) as top_score_value,
        max(case when bottom_row_number = 1 then rank_position end) as bottom_rank_position,
        max(case when bottom_row_number = 1 then score_value end) as bottom_score_value,
        avg(score_value) as avg_score_value
    from ranked
    group by
        world_id,
        collected_at,
        ranking_type
)

select
    world_id,
    collected_at,
    ranking_type,
    entry_count,
    top_guild_id,
    top_guild_name,
    top_score_value,
    bottom_rank_position,
    bottom_score_value,
    avg_score_value
from summary
