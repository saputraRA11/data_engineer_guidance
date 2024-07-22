function main(){
    curl -O https://raw.githubusercontent.com/DataTalksClub/data-engineering-zoomcamp/main/cohorts/2022/week_2_data_ingestion/airflow/docker-compose.yaml;
    mkdir -p ./dags ./logs ./plugins;
    echo -e "AIRFLOW_UID=$(id -u)" > .env;
    docker build .;
    docker compose up airflow-init;
    docker compose up -d;
}

main