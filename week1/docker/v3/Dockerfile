FROM python:3.9

WORKDIR /app

COPY ingestion_data.py ingesting.py

COPY requirement.txt requirement.txt

# run python install module
RUN pip install -r requirement.txt

# for running python
ENTRYPOINT [ "python", "ingesting.py" ]
