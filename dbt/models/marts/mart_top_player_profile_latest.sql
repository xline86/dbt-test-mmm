with ranked as (
    select
        player.world_id,
        player.player_id,
        player.player_name,
        player.current_bp,
        player.player_rank,
        player.quest_id,
        player.tower_id,
        player.guild_id,
        player.guild_name,
        player.guild_position,
        player.prev_legend_league_class,
        player.collected_at,
        row_number() over (
            partition by player.world_id, player.player_id
            order by player.collected_at desc, player.source_file desc
        ) as row_number
    from {{ ref('stg_player_info') }} as player
)

select
    world_id,
    player_id,
    player_name,
    current_bp,
    player_rank,
    quest_id,
    tower_id,
    guild_id,
    guild_name,
    guild_position,
    prev_legend_league_class,
    collected_at
from ranked
where row_number = 1
