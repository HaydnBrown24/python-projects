import requests
import pandas as pd

# Simple Premier League 2022-23 dataset
url = "https://www.football-data.co.uk/mmz4281/2223/E0.csv"

# Download and save
print("Downloading data...")
r = requests.get(url)
r.raise_for_status()  # stop if download fails
open("data/raw/prem_results.csv", "w", encoding="utf-8").write(r.text)

# Load with pandas
df = pd.read_csv("data/raw/prem_results.csv")
print(df.head())
print(df.info)
print(df.shape)
print(df.columns)

# Average goals per game
avg_goals = (df["FTHG"] + df["FTAG"]).mean()
print("Average goals per match : " + str(avg_goals))

# Adding data for 2023-24 season

new_url = "https://www.football-data.co.uk/mmz4281/2324/E0.csv"

# Download and save
print("Downloading data...")
r = requests.get(new_url)
r.raise_for_status()  # stop if download fails
open("data/raw/prem_results24.csv", "w", encoding="utf-8").write(r.text)

# Load with pandas
new_df = pd.read_csv("data/raw/prem_results24.csv")
print(new_df.head())

# Add season column to both dataframes
df["Season"] = "2022/2023"
new_df["Season"] = "2023/2024"

# Append both dataframes
df = pd.concat([df, new_df], ignore_index=True)
print(df.tail())
print(df.shape)

print(df["Season"].value_counts())

# Save as CSV file
df.to_csv("data/raw/prem_combined.csv", index=False)
print("Saved combined data to data/raw/prem_combined.csv")
