from airflow import DAG
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime


with DAG(
    'data_pipeline',
    default_args={'retries': 1},
    schedule_interval='@daily',  # 
    start_date=datetime(2024, 1, 1),
    catchup=False  
) as dag:
    
    # Tache 1 
    validate_hive_fr = BashOperator(
        task_id='validate_hive_fr',
        bash_command="hive -e 'SELECT * FROM data_mining.news_fr LIMIT 10;'"
    )
    
    validate_hive_ar = BashOperator(
        task_id='validate_hive_ar',
        bash_command="hive -e 'SELECT * FROM data_mining.news_ar LIMIT 10;'"
    )

    validate_hive_en = BashOperator(
        task_id='validate_hive_en',
        bash_command="hive -e 'SELECT * FROM data_mining.news_en LIMIT 10;'"
    )

    # Tache 2
    run_spark_job_fr = BashOperator(
        task_id='run_spark_job_fr',
        bash_command="spark-submit /scripts/preprocessing/clean_googlenews.py --lang fr"
    )
    
    run_spark_job_ar = BashOperator(
        task_id='run_spark_job_ar',
        bash_command="spark-submit /scripts/preprocessing/clean_googlenews.py --lang ar"
    )
    
    run_spark_job_en = BashOperator(
        task_id='run_spark_job_en',
        bash_command="spark-submit /scripts/preprocessing/clean_googlenews.py --lang en"
    )
    
    
    validate_hive_fr >> run_spark_job_fr
    validate_hive_ar >> run_spark_job_ar
    validate_hive_en >> run_spark_job_en
