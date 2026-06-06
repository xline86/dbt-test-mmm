{% macro latest_raw_files(source_name) %}
raw_files as (
    select
        collected_at,
        source_file,
        raw_payload,
        raw_payload:data:world_id::number as world_id,
        coalesce(
            regexp_substr(source_file, '_([0-9]+)\\.json$', 1, 1, 'e', 1)::number,
            0
        ) as source_file_suffix
    from {{ source('raw', source_name) }}
),

latest_raw_files as (
    select
        collected_at,
        source_file,
        raw_payload,
        world_id
    from raw_files
    qualify row_number() over (
        partition by world_id, to_date(collected_at)
        order by source_file_suffix desc, source_file desc
    ) = 1
)
{% endmacro %}
