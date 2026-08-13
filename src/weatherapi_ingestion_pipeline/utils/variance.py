import pandas as pd
from datetime import timedelta
from sqlalchemy import text

def last24Hours(engine, current_time_dt):
    range24hrs = current_time_dt - timedelta(hours=24)
    query = text("""
        SELECT temperature_2m, rain, precipitation_probability, relative_humidity_2m, wind_speed_10m 
        FROM hourly_data 
        WHERE forecast_time = :target_date AND consult_time >= :time_limit
    """)
    historical_df = pd.read_sql_query(query, engine, params={"target_date": current_time_dt, "time_limit": range24hrs})
    return historical_df

def apply_variance(hourly_data, current_time_dt, current_values, engine):
    historical_df = last24Hours(engine, current_time_dt)
    varVarianceList = historical_df.mean().fillna(0).to_dict()
    consultTime = hourly_data["date"] == current_time_dt
    for metric, mean_value in varVarianceList.items():
        col = f"{metric}_variance"
        hourly_data[col] = 0.0
        hourly_data.loc[consultTime, col] = round(abs(mean_value - current_values[metric]), 2)
    return hourly_data  