from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
    DefaultScheduleStatus
)

from . import assets

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="all_assets_job"), 
    cron_schedule="0 0 * * *", 
    default_status=DefaultScheduleStatus.RUNNING,
    execution_timezone='America/New_York'
)

daily_weather_schedule = ScheduleDefinition(
    job=define_asset_job(name="weather_job"), 
    cron_schedule=["0 8 * * *", "0 20 * * *"], 
    default_status=DefaultScheduleStatus.RUNNING,
    execution_timezone='America/New_York'
)


defs = Definitions(
    assets=load_assets_from_package_module(assets), 
    schedules=[daily_refresh_schedule, daily_weather_schedule]
)
