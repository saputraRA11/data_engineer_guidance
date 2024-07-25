from pathlib import Path
import pandas as pd
from prefect import flow,task
from prefect_gcp.cloud_storage import GcsBucket

@task(retries=3)
def fetch(dataset_url):
    """Download Data"""
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def transform(df:pd.DataFrame) -> pd.DataFrame:
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def write_local(df:pd.DataFrame,genre,dataset_file):
    path = Path(f'data/{genre}/{dataset_file}.parquet')
    df.to_parquet(path,compression="gzip")
    return path

@task()
def load_gcs(path:str):
    """Upload to Google Cloud Store"""
    gcs = GcsBucket.load("gcs-bucket")
    gcs.upload_from_path(from_path=path,to_path=path)
    return


@flow()
def etl(month,year,genre):
    """ ETL Web to GCS"""
    dataset_file=f"{genre}_tripdata_{year}-{month:02}"
    dataset_url=f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{genre}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    new_df = transform(df)
    path = write_local(new_df,genre,dataset_file)
    load_gcs(path)

@flow()
def main(months: list[int] = [1,2,3],year:int = 2021,genre:str = "yellow"):
    for month in months:
        etl(month,year,genre)

if __name__=="__main__":
    genre = "yellow"
    months = [1,2,3]
    year = 2021
    main(months,year,genre)