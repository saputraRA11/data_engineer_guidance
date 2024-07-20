function main() {
    docker network create data_engineer;
    cd v4 && docker compose up -d;
    cd ../v3 && docker build -t green_taxi_ingest:v001 .;
    URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz";
    docker run -it --network data_engineer green_taxi_ingest:v001 \
    --user=saputra --password=indonesia11 --host=pg-database --port=5432 \
    --database=taxi --table=taxi_green_trips --url="${URL}" --filename=green_taxi --genre=green;
}

main
