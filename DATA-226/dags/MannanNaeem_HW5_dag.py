# stock_data_dag.py
from airflow import DAG
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import pandas as pd

# Load API key from .env
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

# Snowflake configuration
SNOWFLAKE_DATABASE = "USER_DB_BISON"
SNOWFLAKE_SCHEMA = "PUBLIC"
SNOWFLAKE_TABLE = "STOCK_DATA"
SNOWFLAKE_WAREHOUSE = "BISON_QUERY_WH"

with DAG(
    "stock_data_to_snowflake",
    default_args=default_args,
    start_date=datetime(2025, 10, 3),
    schedule="@daily",
    catchup=False,
) as dag:

    @task
    def fetch_stock_data(symbol="MSFT"):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["Time Series (Daily)"]
        df = pd.DataFrame(data).T.reset_index()
        df.columns = ["date", "open", "high", "low", "close", "volume"]
        return df.to_dict(orient="records")

    @task
    def transform_data(data: list):
        for row in data:
            row["open"] = float(row["open"])
            row["high"] = float(row["high"])
            row["low"] = float(row["low"])
            row["close"] = float(row["close"])
            row["volume"] = int(row["volume"])
        return data

    @task
    def load_to_snowflake(data: list):
        hook = SnowflakeHook(snowflake_conn_id="snowflake_conn")
        with hook.get_conn() as conn:
            with conn.cursor() as cur:
                # Activate warehouse, database, and schema
                cur.execute(f"USE WAREHOUSE {SNOWFLAKE_WAREHOUSE};")
                cur.execute(f"USE DATABASE {SNOWFLAKE_DATABASE};")
                cur.execute(f"USE SCHEMA {SNOWFLAKE_SCHEMA};")

                # Create table if it does not exist
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {SNOWFLAKE_TABLE} (
                        DATE DATE,
                        OPEN FLOAT,
                        HIGH FLOAT,
                        LOW FLOAT,
                        CLOSE FLOAT,
                        VOLUME INT
                    );
                """)

                # Clear table before inserting
                cur.execute(f"TRUNCATE TABLE {SNOWFLAKE_TABLE};")

                # Insert rows
                for row in data:
                    cur.execute(
                        f"""
                        INSERT INTO {SNOWFLAKE_TABLE} (DATE, OPEN, HIGH, LOW, CLOSE, VOLUME)
                        VALUES (%s, %s, %s, %s, %s, %s);
                        """,
                        (row["date"], row["open"], row["high"], row["low"], row["close"], row["volume"])
                    )

    # DAG task dependencies
    stock_data = fetch_stock_data()
    transformed_data = transform_data(stock_data)
    load_to_snowflake(transformed_data)