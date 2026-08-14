from api.openmeteo import fetch_openmeteo
from db.connection import db_connect_retry
from utils.clean import thirtyDayCount
from utils.variance import apply_variance
from sqlalchemy.exc import IntegrityError

engine = db_connect_retry()
hourly_data, current_values, current_time_dt = fetch_openmeteo()

hourly_data = apply_variance(hourly_data, current_time_dt, current_values, engine)
hourly_data = hourly_data.rename(columns={"date": "forecast_time"})

try:
    thirtyDayCount(engine)
    hourly_data.to_sql("hourly_data", engine, if_exists="append", index=False)
    print("Success.")
except IntegrityError as e:
    print(f"Skipping, insertion already exists: {e.orig}")
except Exception as e:
    print(f"Error: {e}")
    raise