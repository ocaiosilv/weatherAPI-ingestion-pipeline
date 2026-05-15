from tkinter import dialog

import openmeteo_requests
import csv
import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 47.6062,
	"longitude": -122.3321,
	"hourly": ["temperature_2m", "rain", "precipitation_probability", "relative_humidity_2m", "wind_speed_10m"],
	"models": "gfs_seamless",
	"current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
	"timezone": "America/Los_Angeles",
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
current_relative_humidity_2m = current.Variables(1).Value()
current_wind_speed_10m = current.Variables(2).Value()

print(f"\nCurrent time: {current.Time()}")
print(f"Current temperature_2m: {current_temperature_2m}")
print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
print(f"Current wind_speed_10m: {current_wind_speed_10m}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_rain = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(3).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()

hourly_data = {
	"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	).tz_convert(response.Timezone().decode())
}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["rain"] = hourly_rain
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

current_time = (
    pd.to_datetime(current.Time(), unit="s", utc=True)
    .tz_convert(response.Timezone().decode())
    .strftime("%Y-%m-%d %H")
)
current_time = current_time.rsplit()
file_path = "variance.csv"
dia = int(current_time[0][8:10]) - 1
hora = int(current_time[1])
der = pd.read_csv(file_path)
der.loc[dia, f"t_{hora+1}"] = round(float(hourly_temperature_2m[0]), 2)
der.to_csv(file_path, index=False)


print("linha( dia ): ",current_time[0][8:10], "|| coluna( hora ): " ,current_time[1])

hourly_dataframe = pd.DataFrame(data = hourly_data)
hourly_dataframe.to_csv('hourly_dataframe.csv', index=False)
print("\nHourly data\n", hourly_dataframe)

