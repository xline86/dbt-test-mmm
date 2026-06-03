with latest_snapshot as (
    select max(collected_at) as collected_at
    from {{ ref('stg_player_ranking') }}
)

select
    ranking.collected_at,
    ranking.world_id,
    ranking.ranking_type,
    ranking.rank_position,
    ranking.player_id,
    ranking.player_name,
    ranking.score_value
from {{ ref('stg_player_ranking') }} as ranking
inner join latest_snapshot
    on ranking.collected_at = latest_snapshot.collected_at
