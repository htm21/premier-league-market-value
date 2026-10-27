# Data dictionary

Final dataset: `data/processed/pl_players_2025_26.csv`, built by `src/make_dataset.py` from [transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets) (snapshot of July 2026).

One row per player who played at least one Premier League game in 2025-26 and has a market value on 15 August 2025 and 3 June 2026: 516 players, no duplicate.

## Variables

| Name | Description | Unit | Origin | Use |
|---|---|---|---|---|
| `player_id` | Transfermarkt id of the player | - | `players.player_id` | identifier |
| `name` | Name of the player | - | `players.name` | identifier |
| `club_id` | Transfermarkt id of the last Premier League club the player played for in 2025-26 | - | last `appearances.player_club_id` of the season | identifier |
| `club` | Name of this club | - | `clubs.name` | feature |
| `position` | General position: Goalkeeper, Defender, Midfield or Attack | - | `players.position` | feature |
| `sub_position` | Detailed position (e.g. Centre-Back, Left Winger) | - | `players.sub_position` | feature |
| `international_caps` | Number of games played for the national team | games | `players.international_caps` | feature |
| `age` | Age of the player on 3 June 2026 | years | computed from `players.date_of_birth` | feature |
| `contract_years_left` | Years left on the contract on 3 June 2026 | years | computed from `players.contract_expiration_date` | feature |
| `appearances` | Premier League games played in 2025-26 | games | count of `appearances` rows | feature |
| `minutes_played` | Premier League minutes played in 2025-26 | minutes | sum of `appearances.minutes_played` | feature |
| `goals` | Premier League goals scored in 2025-26 | goals | sum of `appearances.goals` | feature |
| `assists` | Premier League assists in 2025-26 (Transfermarkt counts them more broadly than the official Premier League) | assists | sum of `appearances.assists` | feature |
| `value_end_eur` | Last market value known on 3 June 2026, the end of season update | € | `player_valuations.market_value_in_eur` | **target** |
| `value_start_eur` | Last market value known on 15 August 2025, the start of the season | € | `player_valuations.market_value_in_eur` | not a feature (data leakage) |
| `value_change_eur` | `value_end_eur` - `value_start_eur` | € | computed | not a feature (data leakage) |
| `value_change_pct` | Value change in % of `value_start_eur` | % | computed | not a feature (data leakage) |

The columns `market_value_in_eur` and `highest_market_value_in_eur` of the `players` table are not kept : they contain the answer, so they cannot be used to explain the market value.

## Missing values

The missing values are replaced in `src/make_dataset.py`, so the final dataset has none.

| Name | Missing in the source | Treatment |
|---|---|---| 
| `contract_years_left` | 29 | No contract end date in the source: mostly old players at the end of their contract, so replaced by 0 (contract over). |
| `international_caps` | 18 | Mostly players who never played for their senior national team (e.g. Sean Longstaff, Kiernan Dewsbury-Hall): replaced by 0. |

## Columns not kept

- The red cards: they are missing in the source for 2025-26 (see the data audit notebook).
- The preferred foot, the height, the yellow cards: they are almost not linked to the market value.