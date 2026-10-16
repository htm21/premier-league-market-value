import pandas as pd
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGO_DIR = PROJECT_ROOT / "assets" / "clubs_logo"
LOGO_DIR.mkdir(parents=True, exist_ok=True)

TRANSFERMARKT_LOGOS_URL = "https://www.transfermarkt.fr/images/wappen/head/"

def logos_import() :
    clubs = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "clubs.csv.gz")
    pl_clubs = clubs [
        (clubs["domestic_competition_id"] == "GB1")
        & (clubs["last_season"] == 2025)
    ]

    for club_id in pl_clubs["club_id"] :
        url = TRANSFERMARKT_LOGOS_URL + f"{club_id}.png"
        response = requests.get(url)
        if response.status_code == 200 :
            (LOGO_DIR / f"{club_id}.png").write_bytes(response.content)
        else :
            print(f"Error for club {club_id} : {response.status_code}")

if __name__ == "__main__" :
    logos_import()