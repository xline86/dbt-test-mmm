with player_bp_rankers as (
    select
        player.world_id,
        player.guild_id,
        player.collected_at,
        count(*) as bp_ranker_num,
        max(case when ranking.rank_position = 1 then player.player_id end) as bp_top_player_id,
        max(case when ranking.rank_position = 1 then player.player_name end) as bp_top_player_name,
        max(case when ranking.rank_position = 1 then ranking.score_value end) as bp_top_player_bp
    from {{ ref('stg_player_ranking') }} as ranking
    inner join {{ ref('stg_player_info') }} as player
        on ranking.world_id = player.world_id
        and ranking.player_id = player.player_id
        and ranking.collected_at = player.collected_at
    where ranking.ranking_type = 'bp'
    group by
        player.world_id,
        player.guild_id,
        player.collected_at
),

ranked as (
    select
        guild.world_id,
        guild.guild_id,
        guild.guild_name,
        guild.bp,
        guild.guild_level,
        guild.stock,
        guild.exp,
        guild.num_members,
        guild.leader_id,
        guild.leader_name,
        guild.free_join,
        guild.bp_requirement,
        guild.collected_at,
        player_bp_rankers.bp_ranker_num,
        player_bp_rankers.bp_top_player_name,
        player_bp_rankers.bp_top_player_id,
        player_bp_rankers.bp_top_player_bp,
        row_number() over (
            partition by guild.world_id, guild.guild_id
            order by guild.collected_at desc, guild.source_file desc
        ) as row_number
    from {{ ref('stg_guild_info') }} as guild
    left join player_bp_rankers
        on guild.world_id = player_bp_rankers.world_id
        and guild.guild_id = player_bp_rankers.guild_id
        and guild.collected_at = player_bp_rankers.collected_at
)

select
    world_id,
    guild_id,
    guild_name,
    bp,
    guild_level,
    stock,
    exp,
    num_members,
    leader_id,
    leader_name,
    free_join,
    bp_requirement,
    bp_ranker_num,
    bp_top_player_name,
    bp_top_player_id,
    bp_top_player_bp,
    collected_at
from ranked
where row_number = 1
