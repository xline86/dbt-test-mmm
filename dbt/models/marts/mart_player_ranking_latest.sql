with ranked as (
    select
        ranking.world_id,
        ranking.ranking_type,
        ranking.rank_position,
        ranking.player_id,
        ranking.player_name,
        ranking.score_value,
        ranking.collected_at,
        ranking.source_file,
        player.guild_id,
        row_number() over (
            partition by ranking.world_id, ranking.ranking_type, ranking.rank_position
            order by ranking.collected_at desc, ranking.source_file desc
        ) as row_number
    from {{ ref('stg_player_ranking') }} as ranking
    left join {{ ref('stg_player_info') }} as player
        on ranking.world_id = player.world_id
        and ranking.player_id = player.player_id
        and ranking.collected_at = player.collected_at
),

guild_bp_ranking as (
    select
        world_id,
        guild_id,
        collected_at,
        rank_position as guild_bp_ranking_position
    from {{ ref('stg_guild_ranking') }}
    where ranking_type = 'bp'
)

select
    ranked.world_id,
    ranked.ranking_type,
    ranked.rank_position,
    ranked.player_id,
    ranked.player_name,
    ranked.score_value,
    guild_bp_ranking.guild_bp_ranking_position,
    ranked.collected_at,
    ranked.source_file
from ranked
left join guild_bp_ranking
    on ranked.world_id = guild_bp_ranking.world_id
    and ranked.guild_id = guild_bp_ranking.guild_id
    and ranked.collected_at = guild_bp_ranking.collected_at
where row_number = 1
