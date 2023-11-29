ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION-slim-buster

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
RUN chmod -R 777 /opt/dagster

RUN pip install dagster-webserver dagster-postgres dagster-aws

COPY requirements.txt /
RUN pip install -r requirements.txt --no-cache-dir

# Copy dagster instance YAML to $DAGSTER_HOME
COPY dagster.yaml /opt/dagster/dagster_home/
COPY pyproject.toml /opt/dagster/app

# Copy your code and workspace to /opt/dagster/app
COPY src /opt/dagster/app/src

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]