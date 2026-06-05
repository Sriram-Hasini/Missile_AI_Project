import pandas as pd
import random

rows = []

for _ in range(50):

    row = []

    for col in range(32):

        if col % 4 == 0:
            row.append(random.randint(20, 100))

        elif col % 4 == 1:
            row.append(round(random.uniform(10.0, 60.0), 2))

        elif col % 4 == 2:
            row.append(hex(random.randint(100, 255)))

        else:
            row.append(format(random.randint(0, 255), '08b'))

    rows.append(row)

columns = [f"W{i}" for i in range(32)]

df = pd.DataFrame(rows, columns=columns)

df.to_csv("sample_telemetry.csv", index=False)

print("50-row telemetry file generated successfully.")