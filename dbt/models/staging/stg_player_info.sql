with {{ latest_raw_files('raw_player_ranking_json') }},

raw_player_info as (
    select
        collected_at,
        source_file,
        world_id,
        raw_payload:data:player_info as player_info
    from latest_raw_files
)

select
    raw.collected_at,
    raw.source_file,
    raw.world_id,
    player.value:id::number as player_id,
    player.value:name::string as player_name,
    player.value:bp::number as current_bp,
    player.value:rank::number as player_rank,
    player.value:quest_id::number as quest_id,
    player.value:tower_id::number as tower_id,
    player.value:icon_id::number as icon_id,
    player.value:guild_id::number as guild_id,
    player.value:guild_name::string as guild_name,
    player.value:guild_join_time::number as guild_join_time,
    player.value:guild_position::number as guild_position,
    player.value:prev_legend_league_class::number as prev_legend_league_class
from raw_player_info as raw,
    lateral flatten(input => raw.player_info) as player
