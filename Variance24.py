import pandas as pd
import numpy as np

rows = 24
data = {}

for i in range(1, 25):
    data[f"t_{i}"] = np.zeros(rows)

data[f"variance"] = np.zeros(rows)
df = pd.DataFrame(data)

df.to_csv("variance.csv", index=False)

print(df)