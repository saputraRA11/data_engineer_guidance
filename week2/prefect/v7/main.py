from pathlib import Path
import pandas as pd
from prefect import flow,task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task()
def extract_from_gcs(genre:str,year:int,month:int) -> Path:
    """ Download trip data from GCS """
    file_path = f'{genre}_tripdata_{year}-{month:02}.parquet'
    gcs_path = f'data/{genre}/{file_path}'
    gcs_block = GcsBucket.load("gcs-bucket")
    gcs_block.download_object_to_path(gcs_path,f'data/{file_path}')
    return Path(f"data/{file_path}")

@task()
def read(path:Path) -> pd.DataFrame:
    """read the data into pandas"""
    df = pd.read_parquet(path)
    return df

@task()
def write_bq(df:pd.DataFrame) -> int:
    """Write DataFrame to BigQuery"""
    gcp_credentials_block = GcpCredentials.load("gcp-credentials")

    df.to_gbq(
        destination_table="yellow.rides",
        project_id="gold-bruin-429014-v5",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )
    return len(df)

@flow()
def el_gcs_to_bq(year:int = 2021,month:int = 1,genre:str = "yellow"):
    """ Main ELT flow to load data into Big Query """
    path = extract_from_gcs(genre,year,month)
    df = read(path)
    row_count = write_bq(df)
    return row_count

@flow(log_prints=True)
def main(
    months: list[int] = [1, 2], year: int = 2021, color: str = "yellow"
):
    """Main EL flow to load data into Big Query"""
    total_rows = 0

    for month in months:
        rows = el_gcs_to_bq(year, month, color)
        total_rows += rows

    print(total_rows)

if __name__ == "__main__":
    main(months=[1, 2], year=2021, color="yellow")