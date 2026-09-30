"""Module for writing data to the local datalake directory."""

from logger.log_handler import log
from datetime import timedelta
from typing import Literal
from pathlib import Path
import pendulum


DATALAKE_ROOT = Path("datalake")


def target_date() -> str:
    """Returns the snapshot date in 'YYYY-MM-DD' format (Europe/Paris, previous day before 9am)."""
    now = pendulum.now("Europe/Paris")
    if now.hour < 9:
        now = now - timedelta(days=1)
    return now.strftime("%Y-%m-%d")


def write_to_storage(
    data: bytes, filetype: Literal["parquet", "json", "csv"] = "parquet", root: Path = DATALAKE_ROOT
) -> bool | None:
    """Writes data to `<root>/<filetype>/<date>_data.<filetype>`, skipping existing files."""
    try:
        folder = root / filetype
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{target_date()}_data.{filetype}"

        # Check if the file already exists
        if path.exists():
            log.warning(f"File '{path}' already exists.")
            return None

        path.write_bytes(data)

        log.info(f"Created {path} ({len(data)} bytes)")
        return True
    except OSError as e:
        log.error(f"An error occurred while writing to the datalake: {e}")
        return False
