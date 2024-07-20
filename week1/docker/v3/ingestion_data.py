import pandas as pd
import sqlalchemy as sql
from time import time
import os
import argparse

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table = params.table
    url = params.url
    filename = params.filename
    genre = params.genre

    if genre not in ["yellow","green"]:
        print("Sorry genre doesn't exist now.")
        return

    # create output of file
    if url.endswith('.csv.gz'):
        csv_name = f'{filename}.csv.gz'
    else:
        csv_name = f'{filename}.csv'

    # download file
    os.system(f'wget {url} -O {csv_name}')

    # create connection
    engine = sql.create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

    # create pipeline stream
    df_iter = pd.read_csv(csv_name,iterator=True,chunksize=100000,low_memory=False)

    # get new chunk data
    df = next(df_iter)

    df = transform(df,genre)

    # create table
    df.head(0).to_sql(name=table,con=engine,if_exists='replace')

    while True:
        try: 
            start_time = time()

            # get new chunk data
            df = next(df_iter)

            # transform data
            df = transform(df,genre)
            
            # insert data into database
            df.to_sql(name=table,con=engine,if_exists='append')

            end_time = time()

            print("inserted antoher chunk, took %.3f second" % (end_time - start_time))

        except StopIteration:
            print("Finish to ingesting data into postgres database")
            break

def transform(df:pd.DataFrame,type:str = "yellow"):
    # transform data
    if type == 'yellow':
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    else:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingesting csv data into postgres")

    parser.add_argument('--user',required=True,help="Username for Postgres")
    parser.add_argument('--password',required=True,help="Password for Postgres")
    parser.add_argument('--host',required=True,help="hostname for Postgres")
    parser.add_argument('--port',required=True,help="port for Postgres")
    parser.add_argument('--database',required=True,help="database name of Postgres")
    parser.add_argument('--table',required=True,help="table name of Postgres")
    parser.add_argument('--url',required=True,help="url of csv file")
    parser.add_argument('--filename',required=True,help="filename of csv file")
    parser.add_argument('--genre',required=True,help="genre of csv file ('yellow','green')")

    args = parser.parse_args()

    main(args)