# Premier League 2025-26 - Market value

Can we explain a Premier League player's market value with his profile and his season, and use it to find undervalued players?

This project goes from the raw Transfermarkt data to a random forest model and a Tableau Public dashboard.

**Dashboard:** [Premier League 2025-26 - Market value](https://public.tableau.com/app/profile/ahmad.hatoum/viz/Nouveauclasseur_17930266681260/Marketoverview)

## Data

Source: [transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets) (also on [Kaggle](https://www.kaggle.com/datasets/davidcariboo/player-scores)), a free dataset built from Transfermarkt.

The final dataset has one row per player who played at least one Premier League game in 2025-26: 516 players. The target is the market value on 3 June 2026, the end of season update. Every column is described in [data_dictionary.md](data_dictionary.md).

The raw files are not stored in the repository, they are downloaded with a script (see *How to run*).

## Notebooks

| Notebook | Content |
|---|---|
| `01_data_exploration` | First look at the raw tables |
| `02_data_audit` | Missing values, update dates of the market values, players per club |
| `03_general_analysis` | Market values by club and position, top players |
| `04_combined_analysis` | Market value against age, contract, playing time, goals, club and position |
| `05_regression_model` | Linear regression and random forest, feature importance, error analysis |
| `06_undervalued_overvalued_players` | List of undervalued and overvalued players |

## Results

| Model | MAE (M€) | R² |
|---|---:|---:|
| Dummy model | 18.0 | -0.02 |
| Linear Regression (baseline) | 9.5 | 0.61 |
| Random Forest | **8.7** | **0.75** |

- The random forest explains 75% of the differences in market value, with an average error of 8.7 M€ on the test set.
- Age (41%) and minutes played (32%) drive most of the model, followed by the contract length, the international caps and the club.
- The model is too low for the most expensive players: for the players worth 50 M€ or more, its estimate is on average 26 M€ below their real market value.
- To find the undervalued and overvalued players, each player is estimated by a model that never saw him (out-of-fold predictions, average error of 7.8 M€). With this error as threshold, 49 players with at least 900 minutes are undervalued and 85 overvalued. The undervalued ones are mostly regular starters of smaller clubs, around 25 years old.

The model takes into account only one season and 516 players. Talent, reputation, and injuries are not included in the data. Therefore, a gap is an indication that must be checked, not proof.

## Dashboard

Three views, with filters on position, club and age group:

- **Market overview**: number of players, median value by position and by club.
- **What drives the value**: median value by age group, value against age, feature importance.
- **Undervalued and overvalued**: gap between the estimated and the real value, and the list of players.

The CSV files used by Tableau are in `data/tableau/`.

## Project structure

```
premier-league-market-value/
├── assets/clubs_logo/   # club logos
├── data/
│   ├── raw/             # downloaded files (not versioned)
│   ├── processed/       # final dataset (built by make_dataset.py)
│   └── tableau/         # CSV exports for Tableau Public
├── notebooks/           # analysis notebooks (01 to 06)
├── reports/figures/     # charts exported from the notebooks
├── src/
│   ├── download_data.py
│   ├── download_clubs_logo.py
│   └── make_dataset.py
├── data_dictionary.md
├── requirements.txt
└── README.md
```

## How to run

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the raw data into data/raw/
python src/download_data.py

# 4. Build the final dataset in data/processed/
python src/make_dataset.py

# 5. Launch Jupyter and run the notebooks in order
jupyter notebook
```

## Tools

Python · pandas · scikit-learn · matplotlib / seaborn · Jupyter · Tableau Public
