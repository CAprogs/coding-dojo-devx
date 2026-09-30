"""Main module for ingesting data into the local datalake."""

from logger.log_handler import log
from write_to_storage import write_to_storage
from get_file import get_file_from_url, get_url_from_endpoints
from requests_cache import CachedSession
from datetime import timedelta


def ingest(
    session: CachedSession, endpoints_path: str = "src/ingestion/endpoints.json", filetype: str = "parquet"
) -> bool | None:
    """Ingests data from a specified URL into the local datalake."""
    # Get the URL from endpoints.json
    url = get_url_from_endpoints(endpoints_path=endpoints_path, filetype=filetype)

    # Load the parquet file in memory
    response = get_file_from_url(url=url, session=session)

    log.info(f"Response status: {response['status']}, From cache: {response['from_cache']}")

    if response["response"] is None or response["status"] != 200:
        log.error("No data received from the API.")
        return False

    # Try to write the data to the local datalake
    result = write_to_storage(data=response["response"], filetype=filetype)

    return result


if __name__ == "__main__":
    # Create a reusable requests session with caching
    session = CachedSession(cache_name="pea_cache", backend="filesystem", expire_after=timedelta(days=1))

    result = ingest(session=session)

    if result is True:
        log.info("Ingestion completed successfully.")
    elif result is False:
        log.error("Ingestion failed.")
    else:
        log.warning("Ingestion skipped: file already exists.")
