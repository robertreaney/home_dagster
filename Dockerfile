ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION-slim-buster

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
RUN chmod -R 777 /opt/dagster

RUN pip install dagster dagster-webserver dagster-docker

COPY home_utils-1.0-py3-none-any.whl /
RUN pip install /home_utils-1.0-py3-none-any.whl

COPY dagster.yaml /opt/dagster/dagster_home/
COPY pyproject.toml src workspace.yaml /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

WORKDIR /opt/dagster/app

