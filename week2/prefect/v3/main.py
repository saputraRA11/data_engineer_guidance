from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

# from prefect_gcp import GcpCredentials
@task(retries=3)
def extract_from_gcs(genre:str,year:int,month:int):
    """ Download trip data from """
    file_path = f'{genre}_tripdata_{year}-{month:02}.parquet'
    folder_path="raw"
    gcs_path = f'{folder_path}/{file_path}'

    # https://prefecthq.github.io/prefect-gcp/cloud_storage/#prefect_gcp.cloud_storage.GcsBucket
    gcs_block = GcsBucket.load("gcs-bucket")
    gcs_block.download_object_to_path(gcs_path,f'data/{file_path}')
    return Path(f'data/{file_path}')


@task()
def transform(path:Path) -> pd.DataFrame:
    """ Data Cleaning Example """
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df["passenger_count"].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df

@task()
def write_bq(df: pd.DataFrame) -> None:
    """ Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("gcp-credentials")
    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="gold-bruin-429014-v5",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow(name="ETL_GCP_TO_BQ")
def etl_gcs_to_bq():
    """Main ETL gcs to Big Query"""
    
    genre = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(genre,year,month)
    df = transform(path)
    write_bq(df)

if __name__ == "__main__":
    etl_gcs_to_bq()