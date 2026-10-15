import os
import requests

def download_data(DIR_PATH : str, BASE_URL : str, table : str) -> None:
    """
    Download data from the source and save it to the raw data directory.

    Parameters:
    DIR_PATH (str): The directory path where the data will be saved.
    BASE_URL (str): The base URL from which the data will be downloaded.
    table (str): The name of the table to download.
    """

    os.makedirs(DIR_PATH, exist_ok=True)

    file_path = os.path.join(DIR_PATH, f"{table}.csv.gz")
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        print(f"{table}.csv.gz already exists. Skipping download.")
        return

    url = f"{BASE_URL}{table}.csv.gz"
    response = requests.get(url)

    file_path = os.path.join(DIR_PATH, f"{table}.csv.gz")
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        print(f"{table}.csv.gz already exists. Skipping download.")
        return

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
    DIR_PATH = "../data/raw"

    TABLE_NAME = [
        "competitions", "clubs", "appearances", 
        "players", "player_valuations"
    ]

    for table in TABLE_NAME:
        download_data(DIR_PATH, BASE_URL, table)