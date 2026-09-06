import argparse
import requests      
import json         
import os
from datetime import datetime

def fetch_exchange_rates(api_url: str) -> dict:
    """Fetches the API from the url with fast error handling"""
    try: 
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"CRITICAL: API Request failed: {e}")
        raise 


def land_exchange_rate_file_to_volume(data: dict, volume_path: str,):
    """Lands the JSON data into a hive-style partitioned Unity Catalog volume"""
    try: 
        # Get current time to name our files and folders
        folder_date = datetime.now().strftime("%Y-%m-%d")                  
        file_datetime = datetime.now().strftime("%Y-%m-%d_%H%M%S")        

        # Create the folder path filename path using hive-stye partitioning
        folder_path = f"{volume_path}/date={folder_date}"
        file_name = f"{folder_path}/exchange_rates_{file_datetime}.json"

        # Create directory for current day run data if not exists
        os.makedirs(folder_path, exist_ok=True)

        # Write the data to the file
        with open(file_name, "w") as f:
            json.dump(data, f)

        print(f"INFO: File written to {folder_path}")

    except Exception as e:
        print(f"CRITICAL: File write failed: {e}")
        raise

if __name__ == "__main__":
    # Setup argparse 
    parser = argparse.ArgumentParser(description="Exchange rates to Unity Catalog volume")
    parser.add_argument("--catalog", type=str, default="dev", help="Target catalog name")
    args, _ = parser.parse_known_args()

    # Declare the variables
    api_endpoint = "https://open.er-api.com/v6/latest/USD"
    volume_destination = f"/Volumes/{args.catalog}/landing/exchange_rates"
    
    # Begin  
    print(f"INFO: Starting extraction for catalog: {args.catalog}")
    raw_payload = fetch_exchange_rates(api_endpoint)
    land_exchange_rate_file_to_volume(raw_payload, volume_destination)
    print("INFO: Pipeline completed successfully.")