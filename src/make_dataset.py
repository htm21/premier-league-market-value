import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

PL_ID = "GB1"
LAST_SEASON = 2025
SEASON_START = "2025-07-01"
SEASON_END = "2026-07-01"

# The two dates used to compare the market values (see the data audit notebook).
DATE_1 = "2025-08-15"
DATE_2 = "2026-06-03"

def value_at(valuations, date) :
    """Last known market value of each player at the given date."""
    past = valuations[valuations["date"] <= date].sort_values("date")
    return past.groupby("player_id")["market_value_in_eur"].last()

def make_dataset() -> pd.DataFrame :
    """
    Build one row per player who played in the Premier League in 2025-26 with a market value at both dates,
    with his profile, his Premier League stats of the season and his market value change.
    """
    clubs = pd.read_csv(RAW_DATA_DIR / "clubs.csv.gz")
    players = pd.read_csv(RAW_DATA_DIR / "players.csv.gz")
    valuations = pd.read_csv(RAW_DATA_DIR / "player_valuations.csv.gz")
    appearances = pd.read_csv(RAW_DATA_DIR / "appearances.csv.gz")

    pl_clubs = clubs[
        (clubs["domestic_competition_id"] == PL_ID)
        & (clubs["last_season"] == LAST_SEASON)
    ]

    season = appearances[
        (appearances["competition_id"] == PL_ID)
        & (appearances["date"] >= SEASON_START)
        & (appearances["date"] < SEASON_END)
    ]

    # Only the players who played in the Premier League in 2025-26, with the last Premier League club they played for.
    pl_club = season.sort_values("date").groupby("player_id")["player_club_id"].last()

    pl_players = players[players["player_id"].isin(pl_club.index)].copy()
    pl_players["club_id"] = pl_players["player_id"].map(pl_club).astype(int)
    pl_players = pl_players.merge(pl_clubs[["club_id", "name"]].rename(columns={"name": "club"}), on="club_id")

    dataset = pl_players[[
        "player_id", "name", "club_id", "club", "position", "sub_position", "foot", "height_in_cm",
        "international_caps",
    ]].copy()

    date_of_birth = pd.to_datetime(pl_players["date_of_birth"])
    contract_expiration = pd.to_datetime(pl_players["contract_expiration_date"])
    dataset["age"] = ((pd.Timestamp(DATE_2) - date_of_birth).dt.days / 365.25).round(1)
    dataset["contract_years_left"] = ((contract_expiration - pd.Timestamp(DATE_2)).dt.days / 365.25).round(1)

    # Premier League stats of the season. The red cards are missing for 2025-26, so they are not kept.
    stats = season.groupby("player_id").agg(
        appearances=("appearance_id", "count"),
        minutes_played=("minutes_played", "sum"),
        goals=("goals", "sum"),
        assists=("assists", "sum"),
        yellow_cards=("yellow_cards", "sum"),
    )
    dataset = dataset.merge(stats, left_on="player_id", right_index=True, how="left")
    dataset[stats.columns] = dataset[stats.columns].fillna(0).astype(int)

    dataset["value_start_eur"] = dataset["player_id"].map(value_at(valuations, DATE_1))
    dataset["value_end_eur"] = dataset["player_id"].map(value_at(valuations, DATE_2))

    # Only the players with a valuation at both dates are compared.
    dataset = dataset.dropna(subset=["value_start_eur", "value_end_eur"])
    dataset["value_change_eur"] = dataset["value_end_eur"] - dataset["value_start_eur"]
    dataset["value_change_pct"] = (100 * dataset["value_change_eur"] / dataset["value_start_eur"]).round(1)

    # Same order as the raw players table, so the ties in the rankings are broken the same way.
    return dataset.sort_values("player_id").reset_index(drop=True)

if __name__ == "__main__" :
    dataset = make_dataset()
    file_path = PROCESSED_DATA_DIR / "pl_players_2025_26.csv"
    dataset.to_csv(file_path, index=False)
    print(f"{len(dataset)} players saved to {file_path.relative_to(PROJECT_ROOT)}")
