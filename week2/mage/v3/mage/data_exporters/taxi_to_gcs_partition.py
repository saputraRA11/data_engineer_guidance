import pyarrow as pa
import pyarrow.parquet as pq
import os
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/private/credentials.json"

bucket_name = "terra-bucket-v1"
project_id = "gold-bruin-429014-v5"

table_name = "ny_taxi_data"
root_path = f"{bucket_name}/{table_name}"

@data_exporter
def export_data_to_google_cloud_storage(data, *args, **kwargs) -> None:
   data["tpep_pickup_date"] = data["tpep_pickup_datetime"].dt.date 
   table = pa.Table.from_pandas(data)
   gcs = pa.fs.GcsFileSystem()

   pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['tpep_pickup_date'],
        filesystem=gcs
   )