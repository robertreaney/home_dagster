import requests as r
import logging
import datetime



class WeatherClient:
    url = 'https://api.openweathermap.org/data/2.5/'
    
    def __init__(self, appid:str, lat:float, lon:float, units:str='imperial'):
        self.appid = appid
        self.lat = lat
        self.lon = lon
        self.units = units


    def hit_endpoint(self, endpoint:str='' , method:str='get', params:dict=dict()):
        assert endpoint in ['forecast', 'weather']
        try:
            _params = self._get_params()
            _params.update(params)
            response = getattr(r, method)(self.url + endpoint, params=_params)
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(response.json())
        except Exception as e:
            logging.error(f'WeatherClient failed to hit endpoint with method={method} params={params}\n{e}')

        return response

    def get_current(self):
        current = self.hit_endpoint('weather')
        return self._parse_current(current)
    
    def get_forecast(self, cnt=4):
        forecast = self.hit_endpoint('forecast', params={'cnt': cnt})
        return self._parse_forecast(forecast)

    # PRIVATE METHODS

    def _get_params(self):
        return {
            'appid': self.appid,
            'lat': self.lat,
            'lon': self.lon,
            'units': self.units
        }

    def _parse_current(self, data):
        timestamp = self._parse_timestamp(data['dt'])

        message = (
                f"Date/Time: {timestamp}\n"
                f"Weather: {data['weather'][0]['description']}\n"
                f"Temperature: {data['main']['temp']}°F\n"
                f"Feels Like: {data['main']['feels_like']}°F\n"
                f"Humidity: {data['main']['humidity']}%\n"
                f"Wind: {data['wind']['speed']} ({data['wind']['gust']}) m/h"
            )
        
        return message


    def _parse_forecast(self, data):
        result = []

        for time_point in data['list']:
            keys = [
                'main',
                'weather',
                'wind',
                'dt'
            ]

            temp = {x: time_point[x] for x in keys}
            result.append(temp)

        messages = [
            (
                f"Date/Time: {self._parse_timestamp(x['dt'])}\n"
                f"Weather: {x['weather'][0]['description']}\n"
                f"Temperature: {x['main']['temp']}°F\n"
                f"Feels Like: {x['main']['feels_like']}°F\n"
                f"Humidity: {x['main']['humidity']}%\n"
                f"Wind: {x['wind']['speed']} ({x['wind']['gust']}) m/h"
            )
            for x in result
        ]

        return 'Weather Forecast:\n----\n' + '\n----\n'.join(messages)
    
    def _parse_timestamp(self, date):
        
        def is_dst_in_effect(date):
            # Check if DST is in effect for the given date (North Carolina, USA)
            dst_start = datetime.datetime(date.year, 3, 8)  # Second Sunday in March
            dst_end = datetime.datetime(date.year, 11, 1)   # First Sunday in November

            # Calculate the dates for the start and end of DST
            while dst_start.weekday() != 6:  # Find the second Sunday
                dst_start += datetime.timedelta(days=1)
            while dst_end.weekday() != 6:    # Find the first Sunday
                dst_end += datetime.timedelta(days=1)

            return dst_start <= date < dst_end

        def timestamp_to_est(unix_timestamp):
            # Convert the Unix timestamp to a UTC datetime object
            utc_dt = datetime.datetime.utcfromtimestamp(unix_timestamp)

            # Calculate the EST offset (5 hours)
            est_offset = datetime.timedelta(hours=-5)

            # Check if DST is in effect for the given UTC datetime
            if is_dst_in_effect(utc_dt):
                est_offset += datetime.timedelta(hours=1)  # Add 1 hour for EDT

            # Apply the EST/EDT offset to the UTC datetime to get the EST/EDT time
            est_dt = utc_dt + est_offset

            # Format the EST/EDT datetime as a human-readable string
            formatted_time = est_dt.strftime("%m/%d/%Y %I:%M%p")

            return formatted_time
        
        return timestamp_to_est(date)