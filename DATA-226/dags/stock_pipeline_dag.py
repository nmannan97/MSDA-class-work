import os
import requests
import snowflake.connector
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
SNOWFLAKE_SCHEMA = "RAW"
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")


def extract_alpha_vantage():
    url = "https://www.alphavantage.co/query"
    params = {"function": "TIME_SERIES_DAILY", "symbol": "TSLA", "apikey": API_KEY}
    data = requests.get(url, params=params).json()["Time Series (Daily)"]
    return data


def load_to_snowflake(**context):
    data = context['ti'].xcom_pull(task_ids="extract_task")

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DB,
        schema=SNOWFLAKE_SCHEMA,
        role=SNOWFLAKE_ROLE
    )
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS RAW.MARKET_DATA (
        SYMBOL STRING NOT NULL,
        TRADE_DATE DATE NOT NULL,
        OPEN NUMBER(18,4),
        CLOSE NUMBER(18,4),
        HIGH NUMBER(18,4),
        LOW NUMBER(18,4),
        VOLUME NUMBER(18,0),
        CONSTRAINT PK_MARKET_DATA PRIMARY KEY (SYMBOL, TRADE_DATE)
    );
    """)

    symbol = "TSLA"
    for date, values in data.items():
        cur.execute("""
        MERGE INTO RAW.MARKET_DATA t
        USING (SELECT %s AS SYMBOL,
                      %s AS TRADE_DATE,
                      %s AS OPEN,
                      %s AS CLOSE,
                      %s AS HIGH,
                      %s AS LOW,
                      %s AS VOLUME) s
        ON t.SYMBOL = s.SYMBOL AND t.TRADE_DATE = s.TRADE_DATE
        WHEN MATCHED THEN UPDATE SET
            OPEN = s.OPEN,
            CLOSE = s.CLOSE,
            HIGH = s.HIGH,
            LOW = s.LOW,
            VOLUME = s.VOLUME
        WHEN NOT MATCHED THEN
            INSERT (SYMBOL, TRADE_DATE, OPEN, CLOSE, HIGH, LOW, VOLUME)
            VALUES (s.SYMBOL, s.TRADE_DATE, s.OPEN, s.CLOSE, s.HIGH, s.LOW, s.VOLUME);
        """, (
            symbol, date,
            values["1. open"], values["4. close"],
            values["2. high"], values["3. low"], values["5. volume"]
        ))

    conn.commit()
    cur.close()
    conn.close()


with DAG(
    dag_id="stock_pipeline_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract_alpha_vantage,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load_to_snowflake,
        provide_context=True,
    )

    extract_task >> load_task
