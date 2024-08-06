-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `gold-bruin-429014-v5.yellow.external_yellow_tripdata`
OPTIONS (
  format = 'Parquet',
  uris = [
  'gs://terra-bucket-v1/data/yellow/yellow_tripdata_2021-01.parquet',
  'gs://terra-bucket-v1/data/yellow/yellow_tripdata_2021-02.parquet'
  'gs://terra-bucket-v1/data/yellow/yellow_tripdata_2021-03.parquet',
  'gs://terra-bucket-v1/data/yellow/yellow_tripdata_2021-04.parquet',
  'gs://terra-bucket-v1/data/yellow/yellow_tripdata_2021-05.parquet',
  'gs://terra-bucket-v1/data/yellow/yellow_tripdata_2021-06.parquet'
  ]
);

-- Check yello trip data
SELECT * FROM yellow.external_yellow_tripdata limit 10;

-- create transform table when read data
CREATE OR REPLACE TABLE yellow.external_yellow_v2 AS 
SELECT *, 
DATE(TIMESTAMP_SECONDS(CAST(CAST( tpep_pickup_datetime as INT64)/1000000000 AS INT64))) AS transform_tpep_pickup_datetime,
CAST(VendorID as INT64) as transform_VendorID 
FROM `gold-bruin-429014-v5.yellow.external_yellow_tripdata`

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE gold-bruin-429014-v5.yellow.yellow_tripdata_non_partitoned AS
SELECT * FROM gold-bruin-429014-v5.yellow.external_yellow_v2;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE yellow.yellow_tripdata_partitoned
PARTITION BY
 transform_tpep_pickup_datetime AS
SELECT * FROM yellow.external_yellow_v2;

-- Impact of partition

-- Scanning 1.6GB of data
SELECT DISTINCT(transform_VendorID)
FROM yellow.yellow_tripdata_non_partitoned
WHERE DATE(transform_tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-08-30'

-- -- -- Scanning ~106 MB of DATA
SELECT DISTINCT(transform_VendorID)
FROM yellow.yellow_tripdata_partitoned
WHERE DATE(transform_tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-08-30'


-- Let's look into the partitons
SELECT table_name, partition_id, total_rows
FROM `yellow.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY total_rows DESC;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE yellow.yellow_tripdata_partitoned_clustered
PARTITION BY transform_tpep_pickup_datetime
CLUSTER BY transform_VendorID AS
SELECT * FROM yellow.external_yellow_v2;

-- Query scans 1.1 GB
SELECT count(*) as trips
FROM yellow.yellow_tripdata_partitoned
WHERE DATE(transform_tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-12-31'
  AND transform_VendorID=1;

-- Query scans 864.5 MB
SELECT count(*) as trips
FROM yellow.yellow_tripdata_partitoned_clustered
WHERE DATE(transform_tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-12-31'
  AND transform_VendorID=1;
