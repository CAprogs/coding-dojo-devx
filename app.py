from src.exposition.tables import Table
from src.exposition.main import serve
import dotenv
import os

# Load environment variables from a .env file
dotenv.load_dotenv()

# `just expose` uses the real warehouse, `just expose-ci` the offline one
database = os.getenv("WAREHOUSE_PATH", "warehouse/prod.duckdb")

tables = [
    Table(database=database, schema="gold", name="today_events"),
    Table(database=database, schema="gold", name="nb_events_by_tags"),
]
# run the streamlit app
serve(tables=tables)
