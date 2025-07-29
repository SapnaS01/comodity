import requests
import pandas as pd
import time
from datetime import datetime, timedelta

# 🔑 API config
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
RESOURCE_ID = "35985678-0d79-46b4-9ed6-6f13308a1d24"

# 🎯 Parameters
commodity = "Mango"
state = "Karnataka"
start_date = datetime(2015, 1, 1)
end_date = datetime(2025, 12, 31)

# 📦 Data holders
all_data = []
log_data = []

# 📅 Month-wise loop
current_date = start_date
while current_date <= end_date:
    year = current_date.year
    month = current_date.month
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
            response = requests.get(url)
            status_code = response.status_code

            if status_code == 504:
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

        except requests.exceptions.RequestException:
            break

    # Record fetch status in log
    log_data.append({
        "Date": arrival_date,
        "Commodity": commodity,
        "State": state,
        "Success": fetch_success,
        "HTTP_Status": status_code
    })

    # Move to next month
    next_month = current_date + timedelta(days=32)
    current_date = next_month.replace(day=1)

# 💾 Save data and logs to Excel
if all_data:
    df = pd.DataFrame(all_data)
    df.to_excel("karnataka_mango_new_all_years.xlsx", index=False)

log_df = pd.DataFrame(log_data)
log_df.to_excel("karnataka_mango_fetch_log.xlsx", index=False)
