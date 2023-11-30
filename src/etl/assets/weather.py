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

from home_utils import morning_alert

warnings.filterwarnings("ignore", category=ExperimentalWarning)


@asset(group_name="weather", compute_kind="Python")
def daily() -> None:
    logging.info('Starting Weather Forecast Update')

    morning_alert()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    daily()