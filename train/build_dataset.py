# train/build_dataset.py

import pandas as pd
import os

def build_dataset():
    raw_path = "data/raw_bdl_game_logs.csv"
    if not os.path.exists(raw_path):
        raise Exception("Raw logs missing — run scraper first.")

    df = pd.read_csv(raw_path)

    # Clean names
    df["player_name"] = df["player.first_name"] + " " + df["player.last_name"]

    # Basic columns
    df["points"] = df["pts"]
    df["rebounds"] = df["reb"]
    df["assists"] = df["ast"]
    df["minutes"] = df["min"]

    # Rolling features
    df = df.sort_values(["player_name", "game.date"])

    df["pts_last5"] = df.groupby("player_name")["points"].transform(lambda x: x.rolling(5).mean())
    df["reb_last5"] = df.groupby("player_name")["rebounds"].transform(lambda x: x.rolling(5).mean())
    df["ast_last5"] = df.groupby("player_name")["assists"].transform(lambda x: x.rolling(5).mean())
    df["min_last5"] = df.groupby("player_name")["minutes"].transform(lambda x: x.rolling(5).mean())

    df["pts_avg"] = df.groupby("player_name")["points"].transform("mean")
    df["reb_avg"] = df.groupby("player_name")["rebounds"].transform("mean")
    df["ast_avg"] = df.groupby("player_name")["assists"].transform("mean")
    df["min_avg"] = df.groupby("player_name")["minutes"].transform("mean")

    df.to_csv("data/dataset.csv", index=False)
    print("Saved → data/dataset.csv")

    return df


if __name__ == "__main__":
    build_dataset()
