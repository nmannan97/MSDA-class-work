from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime

with DAG(
    dag_id="etl_raw_sessions_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    description="ETL DAG to load raw session data into Snowflake",
) as dag:

    create_user_session_table = SnowflakeOperator(
        task_id="create_user_session_table",
        sql="""
        CREATE OR REPLACE TABLE raw.user_session_channel (
            user_id STRING,
            session_id STRING,
            channel STRING
        );
        """,
    )

    create_session_timestamp_table = SnowflakeOperator(
        task_id="create_session_timestamp_table",
        sql="""
        CREATE OR REPLACE TABLE raw.session_timestamp (
            session_id STRING,
            session_start TIMESTAMP,
            session_end TIMESTAMP
        );
        """,
    )

    load_user_session_data = SnowflakeOperator(
        task_id="load_user_session_data",
        sql="COPY INTO raw.user_session_channel FROM @my_stage/user_session_channel.csv FILE_FORMAT=(TYPE=CSV);",
    )

    load_session_timestamp_data = SnowflakeOperator(
        task_id="load_session_timestamp_data",
        sql="COPY INTO raw.session_timestamp FROM @my_stage/session_timestamp.csv FILE_FORMAT=(TYPE=CSV);",
    )

    create_user_session_table >> create_session_timestamp_table >> [load_user_session_data, load_session_timestamp_data]
