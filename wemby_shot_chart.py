from src.fetcher import fetch_shot_data
from src.graphing import plot_shot_chart

def main():
    WEMBY_ID = 1641705
    KNICKS_ID = 1610612752
    
    print("Step 1: Grabbing data from NBA API...")
    raw_data = fetch_shot_data(player_id=WEMBY_ID, opponent_id=KNICKS_ID)
    raw_data.to_csv('data/wemby_shots.csv', index=False)

    print("Step 2: Generating the shot chart...")
    plot_shot_chart(raw_data, subject="Victor Wembanyama", filename="wemby_shots")

if __name__ == "__main__":
    main()