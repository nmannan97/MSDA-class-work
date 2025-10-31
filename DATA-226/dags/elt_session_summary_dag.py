from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

SNOWFLAKE_HOOK_PARAMS = {
    "account": "lvb17920",
    "database": "USER_DB_BISON",
    "schema": "RAW",  # make sure schema matches your table
    "warehouse": "BISON_QUERY_WH",
    "role": "PUBLIC"
}

with DAG(
    dag_id="elt_session_summary_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    description="ELT DAG to create session_summary table in Snowflake",
) as dag:

    # Optional: create schema if it doesn't exist
    create_raw_schema = SQLExecuteQueryOperator(
        task_id="create_raw_schema",
        sql="""
        CREATE SCHEMA IF NOT EXISTS "USER_DB_BISON"."RAW";
        """,
        conn_id="snowflake_conn",
        hook_params=SNOWFLAKE_HOOK_PARAMS
    )

    create_user_session_table = SQLExecuteQueryOperator(
        task_id="create_user_session_table",
        sql="""
        CREATE OR REPLACE TABLE "USER_DB_BISON"."RAW"."USER_SESSION_CHANNEL" (
            user_id STRING,
            session_id STRING,
            channel STRING
        );
        """,
        conn_id="snowflake_conn",
        hook_params=SNOWFLAKE_HOOK_PARAMS
    )

    create_raw_schema >> create_user_session_table