from src.fetcher import fetch_shot_data
from src.lineup_processor import filter_shot_chart_by_opponent_presence
from src.graphing import plot_shot_chart

def main():
    SPURS_ID = 1610612759
    KNICKS_ID = 1610612752
    WEMBY_ID = 1641705
    
    print("Step 1: Fetching all Knicks playoff shots against the Spurs...")
    raw_team_shots = fetch_shot_data(team_id=KNICKS_ID, opponent_id=SPURS_ID)
    raw_team_shots.to_csv('data/knicks_shot_data.csv', index=False)
    
    print("Step 2: Filtering shots for Wemby...")
    shots_without_wemby = filter_shot_chart_by_opponent_presence(
        shot_chart_df=raw_team_shots,
        opponent_player_id=WEMBY_ID,
        exclude_player=True
    )
    shots_with_wemby = filter_shot_chart_by_opponent_presence(
        shot_chart_df=raw_team_shots,
        opponent_player_id=WEMBY_ID,
        exclude_player=False
    )
    shots_without_wemby.to_csv('data/knicks_no_wemby.csv', index=False)
    shots_with_wemby.to_csv('data/knicks_with_wemby.csv', index=False)

    print("Step 3: Generating the shot chart...")
    plot_shot_chart(shots_without_wemby, subject="New York Knicks", filename="knicks_no_wemby")
    plot_shot_chart(shots_with_wemby, subject="New York Knicks", filename="knicks_with_wemby")


if __name__ == "__main__":
    main()