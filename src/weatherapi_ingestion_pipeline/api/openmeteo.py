from datetime import datetime, timedelta ## https://www.geeksforgeeks.org/python/python-datetime-timedelta-function/
import openmeteo_requests ## https://open-meteo.com/en/docs
from zoneinfo import ZoneInfo
import pandas as pd
import requests_cache
from retry_requests import retry

def fetch_openmeteo():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)


    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"


    metrics = ["temperature_2m", "rain", "precipitation_probability", "relative_humidity_2m", "wind_speed_10m"]
    models = "gfs_seamless"
    timezone = "America/Los_Angeles"


    params = {
        "latitude": 47.6062,
        "longitude": -122.3321,
        "hourly": metrics,
        "models": models,
        "current": metrics,
        "timezone": timezone,
        "forecast_days": 3,
    }
    responses = openmeteo.weather_api(url, params = params)


    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")


    # Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_rain = 	current.Variables(1).Value()
    current_precipitation_probability = current.Variables(2).Value()
    current_relative_humidity_2m = current.Variables(3).Value()
    current_wind_speed_10m = current.Variables(4).Value()


    print(f"\nCurrent time: {current.Time()}")
    print(f"Current temperature_2m: {current_temperature_2m}")
    print(f"Current rain: {current_rain}")
    print(f"Current precipitation_probability: {current_precipitation_probability}")
    print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
    print(f"Current wind_speed_10m: {current_wind_speed_10m}")


    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_rain = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()


    hourly_data = pd.DataFrame({
        "date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        ).tz_convert(response.Timezone().decode())
    })
    current_time_dt = datetime.fromtimestamp(current.Time(),tz=ZoneInfo("America/Los_Angeles")).replace(minute=0, second=0, microsecond=0)


    hourly_data["consult_time"] = current_time_dt
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["rain"] = hourly_rain
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m


    current_values = {
        "temperature_2m": current_temperature_2m,
        "rain": current_rain,
        "precipitation_probability": current_precipitation_probability,
        "relative_humidity_2m": current_relative_humidity_2m,
        "wind_speed_10m": current_wind_speed_10m
    }
    return hourly_data, current_values, current_time_dt