FROM python:3.9

WORKDIR /app

# run python install module
RUN pip install pandas

COPY pipeline.py pipeline.py

# for running bash
# ENTRYPOINT [ "bash" ]

# for running python
ENTRYPOINT [ "python", "pipeline.py" ]
