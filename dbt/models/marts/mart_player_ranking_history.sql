select
    world_id,
    player_id,
    player_name,
    ranking_type,
    collected_at,
    rank_position,
    score_value,
    source_file
from {{ ref('stg_player_ranking') }}
