import os
import requests
from pathlib import Path

def download_data(dir_path : str, base_url : str, table : str) -> None:
    """
    Download data from the source and save it to the raw data directory.

    Parameters:
    dir_path (str): The directory path where the data will be saved.
    base_url (str): The base URL from which the data will be downloaded.
    table (str): The name of the table to download.
    """

    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, f"{table}.csv.gz")
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        print(f"{table}.csv.gz already exists. Skipping download.")
        return

    url = f"{base_url}{table}.csv.gz"
    response = requests.get(url)

    file_path = os.path.join(dir_path, f"{table}.csv.gz")

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {table}.csv.gz successfully.")
    else:
        print(f"Failed to download {table}.csv.gz. Status code: {response.status_code}")

if __name__ == "__main__":
    print("\033c")
    print("Downloading data from source ...")

    BASE_URL = "https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/"
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DIR_PATH = PROJECT_ROOT / "data" / "raw"

    TABLE_NAME = [
        "competitions", "clubs", "appearances", 
        "players", "player_valuations"
    ]

    for table in TABLE_NAME:
        download_data(DIR_PATH, BASE_URL, table)