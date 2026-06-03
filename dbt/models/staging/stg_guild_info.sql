with raw_guild_info as (
    select
        collected_at,
        source_file,
        raw_payload:data:world_id::number as world_id,
        raw_payload:data:guild_info as guild_info
    from {{ source('raw', 'raw_guild_ranking_json') }}
)

select
    raw.collected_at,
    raw.source_file,
    raw.world_id,
    guild.value:id::number as guild_id,
    guild.value:name::string as guild_name,
    guild.value:bp::number as bp,
    guild.value:level::number as guild_level,
    guild.value:stock::number as stock,
    guild.value:exp::number as exp,
    guild.value:num_members::number as num_members,
    guild.value:leader_id::number as leader_id,
    guild.value:leader_name::string as leader_name,
    guild.value:policy::number as policy,
    guild.value:description::string as description,
    guild.value:free_join::boolean as free_join,
    guild.value:bp_requirement::number as bp_requirement
from raw_guild_info as raw,
    lateral flatten(input => raw.guild_info) as guild
