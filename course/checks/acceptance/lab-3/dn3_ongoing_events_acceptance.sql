-- DN-3 acceptance: ongoing events without detailed occurrences are listed today; future ones are not.
-- Returns the offending sample events (a passing test returns nothing).
WITH expected AS (
    SELECT
        event_id,
        event_id != 900013 AS should_be_listed
    FROM (VALUES (900010), (900011), (900012), (900013)) AS t (event_id)
)

SELECT
    e.event_id,
    e.should_be_listed
FROM expected AS e
LEFT JOIN {{ ref('today_events') }} AS t
    ON e.event_id = t.event_id
WHERE (t.event_id IS NOT NULL) != e.should_be_listed
