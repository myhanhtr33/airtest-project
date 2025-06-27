# log_to_excel.py
import os
import re
import pandas as pd

def convert_latest_log_to_excel(log_dir="logs"):
    log_files = [f for f in os.listdir(log_dir) if f.startswith("log_") and f.endswith(".log")]
    if not log_files:
        print("No log files found.")
        return

    latest_log = sorted(log_files)[-1]
    log_path = os.path.join(log_dir, latest_log)

    pattern = re.compile(
        r"\[(?P<level>\w+)\] (?P<timestamp>[\d\-:\s,]+) - (?P<suite>[^|]+)\| (?P<file>[^|]+)\| (?P<name>[^-]+)- (?P<message>.+)"
    )

    records = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                records.append(match.groupdict())

    if records:
        df = pd.DataFrame(records)
        excel_path = os.path.join(log_dir, latest_log.replace(".log", ".xlsx"))
        df.to_excel(excel_path, index=False)
        print(f"✅ Log exported to Excel: {excel_path}")
    else:
        print("No matching log entries found.")
