"""Generate a small synthetic events sample for offline and CI runs.

All events, venues and contacts are fictional. Dates are relative to the current day so that
`gold.today_events` is never empty. Some rows deliberately exercise the backlog stories
(course/backlog/): an address without street (DN-2) and ongoing events without occurrences (DN-3).
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Any
import duckdb


PARIS = ZoneInfo("Europe/Paris")
OUTPUT = Path(__file__).parent / "events_sample.parquet"


def slot(day: datetime, start_hour: int, duration_hours: int = 2) -> str:
    """Formats one occurrence the way the Paris Open Data API does: `<start>_<end>`."""
    start = day.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=duration_hours)
    return f"{start.isoformat()}_{end.isoformat()}"


def event(idx: int, **overrides: Any) -> dict[str, Any]:
    """Builds one event row with sensible defaults."""
    row: dict[str, Any] = {
        "id": f"sample-{idx:03d}",
        "event_id": 900000 + idx,
        "url": f"https://example.org/events/{idx}",
        "title": f"Sample event {idx}",
        "lead_text": "A fictional event used for offline development.",
        "description": "<p>Fictional description.</p>",
        "date_start": None,
        "date_end": None,
        "occurrences": None,
        "date_description": "Fictional schedule",
        "cover_url": None,
        "cover_credit": None,
        "address_name": "Maison des Exemples",
        "address_street": f"{idx} rue de l'Exemple",
        "address_zipcode": "75011",
        "lon": 2.37 + idx / 1000,
        "lat": 48.86 + idx / 1000,
        "pmr": 0,
        "blind": 0,
        "deaf": 0,
        "sign_language": "0",
        "mental": "0",
        "contact_url": None,
        "contact_phone": None,
        "contact_mail": None,
        "contact_facebook": None,
        "price_type": "gratuit",
        "price_detail": None,
        "access_link": None,
        "access_link_text": None,
        "updated_at": None,
        "programs": None,
        "title_event": None,
        "audience": "Tout public.",
        "rank": float(idx),
        "qfap_tags": "Concert",
        "contact_organisation_name": "DataNova Events (fictional)",
        "contact_url_text": None,
        "contact_instagram": None,
    }
    row.update(overrides)
    return row


def with_slots(idx: int, slots: list[str], **overrides: Any) -> dict[str, Any]:
    """Builds an event whose dates are derived from its occurrences."""
    starts = [datetime.fromisoformat(s.split("_")[0]) for s in slots]
    ends = [datetime.fromisoformat(s.split("_")[1]) for s in slots]
    return event(idx, occurrences=";".join(slots), date_start=min(starts), date_end=max(ends), **overrides)


def build_rows(now: datetime) -> list[dict[str, Any]]:
    """Returns the sample rows for the given reference time."""
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    in_week = today + timedelta(days=7)
    return [
        # Regular events happening later today and in the coming days
        with_slots(1, [slot(today, 23, 1), slot(in_week, 20)], title="Jazz on the canal", qfap_tags="Concert;Nuit"),
        with_slots(2, [slot(today, 23, 1)], title="Night science talk", qfap_tags="Conférence;Sciences", pmr=1),
        with_slots(3, [slot(today, 23, 1), slot(tomorrow, 15)], title="Kids comic workshop", qfap_tags="BD;Enfants"),
        with_slots(4, [slot(today, 23, 1)], title="Improv comedy", qfap_tags="Humour;Théâtre", price_type="payant"),
        with_slots(5, [slot(today, 23, 1)], title="Sign language tour", qfap_tags="Balade urbaine", sign_language="1"),
        with_slots(6, [slot(tomorrow, 18), slot(in_week, 18)], title="Photo walk", qfap_tags="Photo;Balade urbaine"),
        # DN-2: zipcode without street and without venue name
        with_slots(
            7,
            [slot(today, 23, 1)],
            title="Pop-up market",
            qfap_tags="Brocante",
            address_name=None,
            address_street=None,
            address_zipcode="75010",
        ),
        # Venue name only: no street, no zipcode
        with_slots(
            8,
            [slot(today, 23, 1)],
            title="Secret garden reading",
            qfap_tags="Littérature",
            address_street=None,
            address_zipcode=None,
        ),
        # No address at all and no coordinates
        with_slots(
            9,
            [slot(tomorrow, 19)],
            title="Online coding meetup",
            qfap_tags="Numérique",
            address_name=None,
            address_street=None,
            address_zipcode=None,
            lon=None,
            lat=None,
        ),
        # DN-3: ongoing exhibitions without detailed occurrences
        event(
            10,
            title="Street art retrospective",
            qfap_tags="Expo;Art contemporain",
            date_start=today - timedelta(days=30),
            date_end=today + timedelta(days=60),
            blind=1,
        ),
        event(
            11,
            title="Paris maps through time",
            qfap_tags="Expo;Histoire",
            date_start=today - timedelta(days=3),
            date_end=today + timedelta(days=3),
            price_type="payant",
        ),
        event(
            12,
            title="Urban nature trail",
            qfap_tags="Nature",
            date_start=today,
            date_end=today + timedelta(days=1, hours=-1),
        ),
        # Future exhibition without occurrences: must not appear today
        event(
            13,
            title="Winter light festival",
            qfap_tags="Festival",
            date_start=today + timedelta(days=30),
            date_end=today + timedelta(days=45),
        ),
        # Past event: filtered out as outdated
        with_slots(14, [slot(today - timedelta(days=400), 20)], title="Last year's gala", qfap_tags="Danse"),
        # Empty HTML price detail and missing tags
        with_slots(15, [slot(today, 23, 1)], title="Mystery performance", qfap_tags=None, price_detail="<p></p>"),
        with_slots(16, [slot(in_week, 10)], title="Senior yoga", qfap_tags="Sport;Senior", mental="1", deaf=1),
    ]


# Column types aligned with the Paris Open Data parquet export
SCHEMA: dict[str, str] = {
    "id": "VARCHAR",
    "event_id": "BIGINT",
    "url": "VARCHAR",
    "title": "VARCHAR",
    "lead_text": "VARCHAR",
    "description": "VARCHAR",
    "date_start": "TIMESTAMPTZ",
    "date_end": "TIMESTAMPTZ",
    "occurrences": "VARCHAR",
    "date_description": "VARCHAR",
    "cover_url": "VARCHAR",
    "cover_credit": "VARCHAR",
    "address_name": "VARCHAR",
    "address_street": "VARCHAR",
    "address_zipcode": "VARCHAR",
    "lon": "DOUBLE",
    "lat": "DOUBLE",
    "pmr": "BIGINT",
    "blind": "BIGINT",
    "deaf": "BIGINT",
    "sign_language": "VARCHAR",
    "mental": "VARCHAR",
    "contact_url": "VARCHAR",
    "contact_phone": "VARCHAR",
    "contact_mail": "VARCHAR",
    "contact_facebook": "VARCHAR",
    "price_type": "VARCHAR",
    "price_detail": "VARCHAR",
    "access_link": "VARCHAR",
    "access_link_text": "VARCHAR",
    "updated_at": "TIMESTAMPTZ",
    "programs": "VARCHAR",
    "title_event": "VARCHAR",
    "audience": "VARCHAR",
    "rank": "DOUBLE",
    "qfap_tags": "VARCHAR",
    "contact_organisation_name": "VARCHAR",
    "contact_url_text": "VARCHAR",
    "contact_instagram": "VARCHAR",
}


def main() -> None:
    """Writes the sample parquet file next to this script."""
    rows = build_rows(datetime.now(PARIS))
    con = duckdb.connect()
    con.execute(f"CREATE TABLE events ({', '.join(f'{name} {kind}' for name, kind in SCHEMA.items())})")
    placeholders = ", ".join("?" for _ in SCHEMA)
    con.executemany(f"INSERT INTO events VALUES ({placeholders})", [[row[name] for name in SCHEMA] for row in rows])
    con.execute(f"COPY events TO '{OUTPUT}' (FORMAT parquet)")
    print(f"Wrote {len(rows)} rows to {OUTPUT}")  # noqa: T201


if __name__ == "__main__":
    main()
