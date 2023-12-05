from dagster import asset, ExperimentalWarning
import logging
import json
from pathlib import Path
from datetime import datetime
import os
import requests as r
import logging
from dagster import asset, MaterializeResult, AssetSelection, define_asset_job, ScheduleDefinition
import warnings

from home_utils import morning_alert

warnings.filterwarnings("ignore", category=ExperimentalWarning)


@asset(group_name="weather", compute_kind="Python")
def weather_daily() -> None:
    logging.info('Starting Weather Forecast Update')

    morning_alert()

# create jobs from assets
weather_job = define_asset_job(name="weather_job", selection="weather_daily")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    weather_daily()