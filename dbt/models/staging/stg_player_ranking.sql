with {{ latest_raw_files('raw_player_ranking_json') }},

raw_rankings as (
    select
        collected_at,
        source_file,
        world_id,
        raw_payload:data:rankings as rankings
    from latest_raw_files
),

bp as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'bp' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as player_id,
        ranking.value:name::string as player_name,
        ranking.value:bp::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:bp) as ranking
),

player_rank as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'rank' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as player_id,
        ranking.value:name::string as player_name,
        ranking.value:rank::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:rank) as ranking
),

quest as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'quest' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as player_id,
        ranking.value:name::string as player_name,
        ranking.value:quest_id::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:quest) as ranking
),

tower as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'tower' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as player_id,
        ranking.value:name::string as player_name,
        ranking.value:tower_id::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:tower) as ranking
),

tower_red as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'tower_red' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as player_id,
        ranking.value:name::string as player_name,
        ranking.value:tower_id::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:tower_red) as ranking
),

tower_green as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'tower_green' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as player_id,
        ranking.value:name::string as player_name,
        ranking.value:tower_id::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:tower_green) as ranking
),

tower_blue as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'tower_blue' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as player_id,
        ranking.value:name::string as player_name,
        ranking.value:tower_id::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:tower_blue) as ranking
),

tower_yellow as (
    select
        raw.collected_at,
        raw.source_file,
        raw.world_id,
        'tower_yellow' as ranking_type,
        ranking.index + 1 as rank_position,
        ranking.value:id::number as player_id,
        ranking.value:name::string as player_name,
        ranking.value:tower_id::number as score_value
    from raw_rankings as raw,
        lateral flatten(input => raw.rankings:tower_yellow) as ranking
)

select * from bp
union all
select * from player_rank
union all
select * from quest
union all
select * from tower
union all
select * from tower_red
union all
select * from tower_green
union all
select * from tower_blue
union all
select * from tower_yellow
