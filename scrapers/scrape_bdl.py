import os
import requests
import pandas as pd

BDL_API_KEY = "7f4db7a9-c34e-478d-a799-fef77b9d1f78"   # ⛔️ PASTE YOUR KEY HERE (7f4d...f78)

BASE = "https://api.balldontlie.io/v1"

HEADERS = {
    "Authorization": f"Bearer {BDL_API_KEY}"
}

def scrape_logs(season=2025, per_page=100):
    """
    Pulls full NBA season stats from BallDon'tLie using ALL-STAR tier.
    """
    print("📥 Fetching NBA season logs from BallDontLie...")

    all_rows = []
    page = 1

    while True:
        url = f"{BASE}/stats"
        params = {
            "seasons[]": season,
            "per_page": per_page,
            "page": page
        }

        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()

        stats = data.get("data", [])
        if not stats:
            break

        for s in stats:
            row = {
                "player_name": s["player"]["first_name"] + " " + s["player"]["last_name"],
                "player_id": s["player"]["id"],
                "game_id": s["game"]["id"],
                "date": s["game"]["date"],
                "min": s["min"],
                "pts": s["pts"],
                "reb": s["reb"],
                "ast": s["ast"],
                "blk": s["blk"],
                "stl": s["stl"],
                "fg3m": s["fg3m"],
                "turnover": s["turnover"],
                "team": s["team"]["abbreviation"],
                "opponent": s["game"]["home_team_id"] if s["team"]["id"] != s["game"]["home_team_id"] else s["game"]["visitor_team_id"]
            }
            all_rows.append(row)

        print(f"Page {page} done...")
        page += 1

    df = pd.DataFrame(all_rows)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/raw_logs.csv", index=False)
    print("✅ Saved → data/raw_logs.csv")
    return df

if __name__ == "__main__":
    scrape_logs()
