from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

SNOWFLAKE_HOOK_PARAMS = {
    "account": "lvb17920",
    "database": "USER_DB_BISON",
    "schema": "RAW",
    "warehouse": "BISON_QUERY_WH",
    "role": "PUBLIC"  # okay for testing
}

with DAG(
    dag_id="etl_raw_sessions_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    description="ETL DAG to load raw session data into Snowflake",
) as dag:

    # 1️⃣ Drop and recreate USER_SESSION_CHANNEL table
    drop_user_session_table = SQLExecuteQueryOperator(
        task_id="drop_user_session_table",
        sql='DROP TABLE IF EXISTS "USER_DB_BISON"."RAW"."USER_SESSION_CHANNEL";',
        conn_id="snowflake_conn",
        hook_params=SNOWFLAKE_HOOK_PARAMS
    )

    create_user_session_table = SQLExecuteQueryOperator(
        task_id="create_user_session_table",
        sql="""
            CREATE TABLE IF NOT EXISTS "USER_DB_BISON"."RAW"."USER_SESSION_CHANNEL" (
                user_id STRING,
                session_id STRING,
                channel STRING
            );
        """,
        conn_id="snowflake_conn",
        hook_params=SNOWFLAKE_HOOK_PARAMS
    )

    # 2️⃣ Drop and recreate SESSION_TIMESTAMP table
    drop_session_timestamp_table = SQLExecuteQueryOperator(
        task_id="drop_session_timestamp_table",
        sql='DROP TABLE IF EXISTS "USER_DB_BISON"."RAW"."SESSION_TIMESTAMP";',
        conn_id="snowflake_conn",
        hook_params=SNOWFLAKE_HOOK_PARAMS
    )

    create_session_timestamp_table = SQLExecuteQueryOperator(
        task_id="create_session_timestamp_table",
        sql="""
            CREATE TABLE IF NOT EXISTS "USER_DB_BISON"."RAW"."SESSION_TIMESTAMP" (
                session_id STRING,
                session_start TIMESTAMP,
                session_end TIMESTAMP
            );
        """,
        conn_id="snowflake_conn",
        hook_params=SNOWFLAKE_HOOK_PARAMS
    )

    # 3️⃣ Load data into USER_SESSION_CHANNEL
    load_user_session_data = SQLExecuteQueryOperator(
        task_id="load_user_session_data",
        sql="""
            COPY INTO "USER_DB_BISON"."RAW"."USER_SESSION_CHANNEL"
            FROM @my_stage/user_session_channel.csv
            FILE_FORMAT=(TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"');
        """,
        conn_id="snowflake_conn",
        hook_params=SNOWFLAKE_HOOK_PARAMS
    )

    # 4️⃣ Load data into SESSION_TIMESTAMP
    load_session_timestamp_data = SQLExecuteQueryOperator(
        task_id="load_session_timestamp_data",
        sql="""
            COPY INTO "USER_DB_BISON"."RAW"."SESSION_TIMESTAMP"
            FROM @my_stage/session_timestamp.csv
            FILE_FORMAT=(TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"');
        """,
        conn_id="snowflake_conn",
        hook_params=SNOWFLAKE_HOOK_PARAMS
    )

    # ✅ Dependencies (no list-to-list errors)
    drop_user_session_table >> create_user_session_table >> load_user_session_data
    drop_session_timestamp_table >> create_session_timestamp_table >> load_session_timestamp_data