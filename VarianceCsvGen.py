import os
import pandas as pd

variables = [
    "temperature_2m",
    "rain",
    "precipitation_probability",
    "relative_humidity_2m",
    "wind_speed_10m"
]
rows = []
for w in range(1, 31):
    row = {
        "Days": f"Day {w}"
    }
    for variable in variables:
        row[f"{variable}_variance"] = 0.0
    rows.append(row)
df = pd.DataFrame(rows)
folder = "30daysVariance"
os.makedirs(folder, exist_ok=True)
df.to_csv(f"{folder}/Variance.csv", index=False)