import pandas as pd
import random

subsystems = {
    "CMD_A": "Propulsion",
    "CMD_B": "Thermal",
    "CMD_C": "Navigation",
    "CMD_D": "Structural",
    "CMD_E": "Power"
}

rows = []

for i in range(200):

    command_prefix = random.choice(
        list(subsystems.keys())
    )

    row = {
        "Command": f"{command_prefix}_{i+1:03d}"
    }

    for j in range(32):

        if j % 4 == 0:

            row[f"W{j}"] = random.randint(
                20,
                100
            )

        elif j % 4 == 1:

            row[f"W{j}"] = round(
                random.uniform(
                    10,
                    60
                ),
                2
            )

        elif j % 4 == 2:

            row[f"W{j}"] = hex(
                random.randint(
                    100,
                    255
                )
            )

        else:

            row[f"W{j}"] = format(
                random.randint(
                    0,
                    255
                ),
                "08b"
            )

    rows.append(row)

df = pd.DataFrame(rows)

df.to_csv(
    "sample_telemetry.csv",
    index=False
)

print(
    "sample_telemetry.csv generated successfully"
)