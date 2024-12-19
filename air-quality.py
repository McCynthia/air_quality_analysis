import requests
import pandas as pd

# API url for air quality in the US
url = "https://api.openaq.org/v2/locations?country=US"
headers = {
    "X-API-Key": "d9c9a021bce0cfcb0e7965caff35fc3770e5998f28c80fa2907d61a0007603c8"
}

response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Getting the results
    locations = data.get("results", [])
    # Making a DataFrame
    processed_data = [
        {
            "city": loc.get("city", "N/A"),
            "location": loc.get("name", "N/A"),
            "country": loc.get("country", "N/A"),
            "pollutants": [param.get("parameter", "N/A") for param in loc.get("parameters", [])],
            "last_updated": loc.get("lastUpdated", "N/A"),
        }
        for loc in locations
    ]
    df = pd.DataFrame(processed_data)

    # Save to CSV
    df.to_csv("us_air_quality_data.csv", index=False)
