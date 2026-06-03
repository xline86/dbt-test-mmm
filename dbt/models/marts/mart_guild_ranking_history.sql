select
    world_id,
    guild_id,
    guild_name,
    ranking_type,
    collected_at,
    rank_position,
    score_value,
    source_file
from {{ ref('stg_guild_ranking') }}
