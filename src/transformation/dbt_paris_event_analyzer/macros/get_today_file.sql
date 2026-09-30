{% macro get_today_file(filetype) %}
    {% set tz = modules.pytz.timezone('Europe/Paris') %}
    {% set run_dt = run_started_at.astimezone(tz) %}

    {% if run_dt.hour < 9 %}
        {% set target_dt = run_dt - modules.datetime.timedelta(days=1) %}
    {% else %}
        {% set target_dt = run_dt %}
    {% endif %}

    {% set date_str = target_dt.strftime('%Y-%m-%d') %}
    {% set filepath = 'datalake/' ~ filetype ~ '/' ~ date_str ~ '_data.' ~ filetype %}
    {{ return(filepath) }}
{% endmacro %}
