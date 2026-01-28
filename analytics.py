import csv
import os
from datetime import datetime

ANALYTICS_FILE = "analytics.csv"

def log_analytics(input_value, prediction, model_version):
    file_exists = os.path.isfile(ANALYTICS_FILE)

    with open(ANALYTICS_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "input_value",
                "prediction",
                "model_version",
                "timestamp"
            ])

        writer.writerow([
            input_value,
            prediction,
            model_version,
            datetime.now().isoformat()
        ])
