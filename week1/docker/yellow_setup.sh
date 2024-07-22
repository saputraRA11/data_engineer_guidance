function main() {
    docker network create data_engineer;
    cd v4 && docker compose up -d;
    cd ../v3 && docker build -t yellow_taxi_ingest:v001 .;
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz";
    docker run -it --network data_engineer yellow_taxi_ingest:v001 \
    --user=saputra --password=indonesia11 --host=pg-database --port=5432 \
    --database=taxi --table=taxi_yellow_trips --url="${URL}" --filename=yellow_taxi --genre=yellow;
}

main
