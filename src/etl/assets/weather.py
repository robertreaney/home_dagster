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

from home_utils import WeatherClient, GmailClient, EmailData, get_secret

warnings.filterwarnings("ignore", category=ExperimentalWarning)


@asset(group_name="weather", compute_kind="Python")
def daily() -> None:
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

    # send forecast as email to user
    secret = get_secret('dev/tokens/helpful')
    for key, value in secret.items():
        os.environ[key] = value

    logging.info('logging into email to listen for messages')
    # load gmail client
    google_client = GmailClient()

    google_client.send_message(
        to='3863663150@mms.att.net', 
        subject=None, 
        message_text=weather + '\n\n' + forecast, 
        thread_id=None, 
        in_reply_to=None)

    return 

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    daily()