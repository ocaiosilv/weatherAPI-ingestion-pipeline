import datetime

def hoursVarianceVarReads(df, current_time):
    metrics = [
        "temperature_2m",
        "rain",
        "precipitation_probability",
        "relative_humidity_2m",
        "wind_speed_10m"
    ]

    range24hrs = current_time - datetime.timedelta(hours=24)

    # Pega só as linhas onde date == current_time e consult_time nas últimas 24h
    last24hourpred = (df["date"] == current_time) & (df["consult_time"] >= range24hrs)
    filtered = df[last24hourpred]

    metric_means = {}
    for metric in metrics:
        values = filtered[metric].dropna().tolist()
        if values:
            metric_means[metric] = sum(values) / len(values)
        else:
            metric_means[metric] = 0

    return metric_means

def apply_variance(hourly_data, current_time_dt,current_values):
    varVarianceList = hoursVarianceVarReads(hourly_data, current_time_dt)
    consultTime = hourly_data["date"] == current_time_dt
    for metric, mean_value in varVarianceList.items():
        col = f"{metric}_variance"
        hourly_data[col] = 0.0
        hourly_data.loc[consultTime, col] = round(abs(mean_value - current_values[metric]), 2)
    return hourly_data  