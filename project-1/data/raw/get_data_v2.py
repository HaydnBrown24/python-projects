# combine_10_seasons.py
import os
import io
import requests
import pandas as pd

os.makedirs("data/raw", exist_ok=True)

LEAGUE = "E0"  # Premier League. (Change to E1=Championship, SP1=La Liga, I1=Serie A, D1=Bundesliga, etc.)
START_YEARS = list(range(2015, 2025))  # 2015/16 ... 2024/25  (10 seasons)


def season_code(y: int) -> str:
    """e.g., 2015 -> '1516' (matches Football-Data URL scheme)."""
    return f"{str(y)[-2:]}{str(y + 1)[-2:]}"


def season_label(y: int) -> str:
    """e.g., 2015 -> '2015/16' for readability."""
    return f"{y}/{str(y + 1)[-2:]}"


def season_url(y: int, league: str) -> str:
    return f"https://www.football-data.co.uk/mmz4281/{season_code(y)}/{league}.csv"


frames = []
for y in START_YEARS:
    label = season_label(y)
    url = season_url(y, LEAGUE)
    local_path = f"data/raw/{LEAGUE}_{season_code(y)}.csv"

    # Cache to disk so you don't re-download every run
    if not os.path.exists(local_path):
        print(f"↓ {label}: {url}")
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        r.raise_for_status()
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(r.text)
    else:
        print(f"✔ cached: {local_path}")

    # Load into memory
    df = pd.read_csv(local_path)
    df["Season"] = label
    frames.append(df)

# One fast concat (more efficient than repeated appends)
combined = pd.concat(frames, ignore_index=True)

print(f"✅ Combined shape: {combined.shape}")
print(combined[["Season", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]].head())

# Optional: save for reuse
combined.to_csv("data/raw/prem_10seasons_combined.csv", index=False)
# Or Parquet (smaller/faster) if you have pyarrow installed:
# combined.to_parquet("data/raw/prem_10seasons_combined.parquet", index=False)
