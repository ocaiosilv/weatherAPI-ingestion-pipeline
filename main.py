
from datetime import datetime, timedelta ## https://www.geeksforgeeks.org/python/python-datetime-timedelta-function/
import openmeteo_requests ## https://open-meteo.com/en/docs
import os
from zoneinfo import ZoneInfo
import pandas as pd
import requests_cache
from retry_requests import retry

def thirtyDayCount():
    file_path = os.path.join("30daysReg")
    if not os.path.exists(file_path):
        os.makedirs(folder, exist_ok=True)
    else:
        for file in os.listdir(file_path):
            thirtyArr = []
            fileTarget = os.path.basename(file).split('-')
            ano, mes, dia = fileTarget[1].split("M")[0], fileTarget[2].split("D")[0], fileTarget[2].split("D")[1]
            thirtyArr.append((int(ano), int(mes), int(dia), file))

        #no loop because the code will run every day( in thesis )
        if len(thirtyArr) > 30:
            menor_data = min(thirtyArr)
            older = menor_data[3]
            os.remove(os.path.join(file_path, older))

def prev24count(ano, mes, dia, hora):
    prev_hours = []

    current = datetime(ano, mes, dia, hora)

    for i in range(1, 25):
        prev = current - timedelta(hours=i)

        prev_hours.append((
            prev.year,
            prev.month,
            prev.day,
            prev.hour
        ))

    return prev_hours



def hoursVarianceVarReads(ano, mes, dia, hora):
    metrics = [
        "temperature_2m",
        "rain",
        "precipitation_probability",
        "relative_humidity_2m",
        "wind_speed_10m"
    ]

    metric_values = {}
    for i in metrics:
        metric_values[i] = []

    hours_list = prev24count(ano, mes, dia, hora)

    for a, m, d, h in hours_list:
        path = f"30daysReg/A-{a}M-{m}D{d}-H{h}.csv"
        if os.path.exists(path):

            df = pd.read_csv(path, parse_dates=["date"])

            df["date"] = pd.to_datetime(df["date"], utc=True).dt.tz_convert(ZoneInfo("America/Los_Angeles"))
            target_time = pd.Timestamp(year=a, month=m, day=d, hour=h, tzinfo=ZoneInfo("America/Los_Angeles"))
            match = df.loc[df["date"] == target_time]

            if match.empty:
                continue

            for metric in metrics:
                value = float(match.iloc[0][metric])
                metric_values[metric].append(value)

    metric_means = {}

    for metric in metrics:
        values = metric_values[metric]
        if values:
            metric_means[metric] = sum(values) / len(values)
        else:
            metric_means[metric] = 0

    return metric_values, metric_means





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

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["rain"] = hourly_rain
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

current_time_dt = datetime.fromtimestamp(current.Time(),tz=ZoneInfo("America/Los_Angeles")).replace(minute=0, second=0, microsecond=0)
ano = current_time_dt.year
mes = current_time_dt.month
dia = current_time_dt.day
hora = current_time_dt.hour
varVarianceList = hoursVarianceVarReads(ano, mes, dia, hora)[1]


for metric, value in varVarianceList.items():
    metric_variance_col = f"{metric}_variance"
    hourly_data[metric_variance_col] = 0.0
    variance_value = round(abs(value -  locals()[f"current_{metric}"]),2)
    hourly_data.loc[dia, metric_variance_col] = variance_value

for folder in ["30daysReg"]:
    thirtyDayCount()
    hourly_data.to_csv(f"30daysReg/A-{ano}M-{mes}D{dia}-H{hora}.csv", index=False)
