from api.openmeteo import fetch_openmeteo
from db.connection import db_connect
from utils.clean import thirtyDayCount
from utils.variance import apply_variance

hourly_data, current_values, current_time_dt = fetch_openmeteo()
hourly_data = apply_variance(hourly_data, current_values, current_time_dt)
engine = db_connect()

try:
    thirtyDayCount()
    hourly_data.to_sql("hourly_data",engine,if_exists="append",index=False)
    print("Success.")
except Exception as error:
    print("Table does not exist. \nPlease follow the correct README instructions.")
    print(error)