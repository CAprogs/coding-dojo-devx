-- DN-2 acceptance: no blank-padded or meaningless address, and no map pin without an address.
-- Returns the offending rows (a passing test returns nothing).
SELECT
    id,
    full_address,
    latitude
FROM {{ ref('up_to_date_events') }}
WHERE
    full_address != trim(full_address)
    OR trim(full_address) = ''
    OR (full_address IS NULL AND (latitude IS NOT NULL OR longitude IS NOT NULL))
    OR (id IN ('sample-007', 'sample-008') AND full_address IS NOT NULL)
