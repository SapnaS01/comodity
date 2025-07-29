import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os

API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
RESOURCE_ID = "35985678-0d79-46b4-9ed6-6f13308a1d24"

# Global Date Range Constants
START_DATE = datetime(2015, 1, 1)
END_DATE = datetime(2025, 12, 31)

def fetch_commodity_data(commodity, state, start_date, end_date):
    all_data = []
    log_data = []
    current_date = start_date

    while current_date <= end_date:
        arrival_date = current_date.replace(day=1).strftime("%Y-%m-%d")
        offset = 0
        fetch_success = False
        status_code = None

        while True:
            url = (
                f"https://api.data.gov.in/resource/{RESOURCE_ID}"
                f"?api-key={API_KEY}"
                f"&format=json"
                f"&filters[Commodity]={commodity}"
                f"&filters[State]={state}"
                f"&filters[Arrival_Date]={arrival_date}"
                f"&limit=1000"
                f"&offset={offset}"
            )

            try:
                response = requests.get(url, timeout=10)
                status_code = response.status_code

                if status_code in [504, 429]:
                    time.sleep(5)
                    continue
                elif status_code != 200:
                    break

                records = response.json().get("records", [])

                if not records:
                    break

                for record in records:
                    record["Queried_Commodity"] = commodity
                    record["Queried_Date"] = arrival_date
                    all_data.append(record)

                fetch_success = True
                offset += 1000
                time.sleep(0.5)

            except (requests.exceptions.RequestException, ValueError):
                break

        log_data.append({
            "Date": arrival_date,
            "Commodity": commodity,
            "State": state,
            "Success": fetch_success,
            "HTTP_Status": status_code
        })

        next_month = current_date + timedelta(days=32)
        current_date = next_month.replace(day=1)

    return all_data, log_data

# Commodity List
commodities = ["Rose(Local)"]  

state = "Karnataka"

# Create Output Folder
os.makedirs("output", exist_ok=True)
os.makedirs("output\logs", exist_ok=True)

def sanitize_filename(name):
    return name.replace('/', '_')

for commodity in commodities:
    print(f"🔄 Fetching data for {commodity} ({START_DATE.date()} ➡ {END_DATE.date()})")
    data, logs = fetch_commodity_data(commodity, state, START_DATE, END_DATE)

    date_range_str = f"{START_DATE.strftime('%Y-%m-%d')}_{END_DATE.strftime('%Y-%m-%d')}"
    safe_commodity = sanitize_filename(commodity)

    if data:
        pd.DataFrame(data).to_excel(f"output/{safe_commodity}_{date_range_str}_data.xlsx", index=False)

    pd.DataFrame(logs).to_excel(f"output/logs/{safe_commodity}_{date_range_str}_fetch_log.xlsx", index=False)

print("✅ All data fetched and saved.")


