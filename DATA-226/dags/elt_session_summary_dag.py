from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime

with DAG(
    dag_id="elt_session_summary_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    description="ELT DAG to join raw tables into analytics.session_summary",
) as dag:

    create_session_summary = SnowflakeOperator(
        task_id="create_session_summary",
        sql="""
        CREATE OR REPLACE TABLE analytics.session_summary AS
        SELECT
            usc.user_id,
            usc.channel,
            st.session_id,
            st.session_start,
            st.session_end,
            DATEDIFF('minute', st.session_start, st.session_end) AS session_duration_min
        FROM raw.user_session_channel usc
        JOIN raw.session_timestamp st
        ON usc.session_id = st.session_id
        QUALIFY ROW_NUMBER() OVER (PARTITION BY usc.session_id ORDER BY st.session_start DESC) = 1;
        """,
    )
