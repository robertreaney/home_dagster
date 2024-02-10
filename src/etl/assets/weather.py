from dagster import asset, ExperimentalWarning
import logging
import json
from pathlib import Path
from datetime import datetime
import os
import requests as r
import logging
from dagster import asset, MaterializeResult
import warnings

from src.etl.utils.weather import WeatherClient
from src.etl.utils.sns import publish_sns_message

warnings.filterwarnings("ignore", category=ExperimentalWarning)

@asset(group_name="weather", compute_kind="Python")
def weather() -> None:
    logging.info('Starting Weather Forecast Update')

    client = WeatherClient(
        appid=os.getenv("OPEN_WEATHER_MAP_API_KEY"),
        lat=os.getenv('LAT'),
        lon=os.getenv('LON')
        )

    weather = client.get_current()
    logging.info(weather)

    forecast = client.get_forecast()
    logging.info(forecast)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    publish_sns_message(
        subject=f'Weather Update {timestamp}',
        message = f'{weather} \n\n~~~~~~~~~~~~~\n {forecast}'
    )

    # this return object provides more information to the workflow
    return MaterializeResult(
        metadata={
            'timestamp': timestamp,
            'cwd': str(Path.cwd())
        }
    )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    weather()