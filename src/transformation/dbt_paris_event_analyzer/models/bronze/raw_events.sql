{% if target.name == 'ci' %}

    -- Offline sample: coordinates are stored as plain columns and rebuilt as a geometry
    SELECT
        * EXCLUDE (lon, lat),
        st_point(lon, lat) AS lat_lon
    FROM read_parquet('data/sample/events_sample.parquet')

{% else %}

    SELECT *
    FROM read_parquet('{{ get_today_file("parquet") }}')

{% endif %}
