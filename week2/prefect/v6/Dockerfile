FROM prefecthq/prefect:2.7.7-python3.9

COPY docker-requirements.txt requirements.txt

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY . /opt/prefect/flows
COPY data /opt/prefect/data