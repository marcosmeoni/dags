from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.git_operator import GitOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'clone_and_deploy_dag',
    default_args=default_args,
    description='Clone a repository and deploy with Helmfile',
    schedule_interval='0 8 * * *',
)

clone_repo = GitOperator(
    task_id='clone_repo',
    git_conn_id='git_default',
    repo='https://github.com/tu-usuario/tu-repo.git',
    branch='main',
    destination='/ruta/de/destino',
    dag=dag,
)

deploy_with_helm = BashOperator(
    task_id='deploy_with_helm',
    bash_command='cd /ruta/de/destino && helmfile -e stg -l release-name=microservices-api-devops-sre-demo --debug apply',
    dag=dag,
)

clone_repo >> deploy_with_helm
