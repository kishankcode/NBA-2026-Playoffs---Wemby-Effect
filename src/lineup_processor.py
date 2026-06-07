import pandas as pd
import time
from nba_api.stats.endpoints import gamerotation

def filter_shot_chart_by_opponent_presence(shot_chart_df, opponent_player_id, exclude_player=True):
    """
    Filters a team's shot chart data based on whether a specific opponent player 
    was active on the court when the shot occurred.
    """
    
    if shot_chart_df.empty:
        return shot_chart_df
        
    # Helper function to convert NBA API remaining period time into absolute game tenths of a second
    def calculate_game_tenths(row):
        period = int(row['PERIOD'])
        min_rem = int(row['MINUTES_REMAINING'])
        sec_rem = int(row['SECONDS_REMAINING'])
        
        # Standard NBA game: Quarters 1-4 are 12 mins. Overtime (5+) is 5 mins.
        if period <= 4:
            elapsed_in_period = (12 * 60) - (min_rem * 60 + sec_rem)
            total_seconds = ((period - 1) * 12 * 60) + elapsed_in_period
        else:
            elapsed_in_period = (5 * 60) - (min_rem * 60 + sec_rem)
            total_seconds = (4 * 12 * 60) + ((period - 5) * 5 * 60) + elapsed_in_period
            
        return total_seconds * 10 # NBA API rotation endpoints track time in tenths of a second

    # Create working copy and map the true game time for every shot
    df = shot_chart_df.copy()
    df['SHOT_TIME_TENTHS'] = df.apply(calculate_game_tenths, axis=1)
    df['PLAYER_ON_COURT'] = False
    
    unique_games = df['GAME_ID'].unique()
    
    # Process game-by-game to avoid duplicate network overhead
    for game_id in unique_games:
        try:
            # Fetch exact lineup substitution timelines for the game
            rot_data = gamerotation.GameRotation(game_id=game_id)
            
            # Combine home and away rotation datasets safely
            full_rotation = pd.concat(rot_data.get_data_frames(), ignore_index=True)
            
            # Extract player stints
            player_stints = full_rotation[full_rotation['PERSON_ID'] == opponent_player_id]
            
            if player_stints.empty:
                continue
                
            game_mask = df['GAME_ID'] == game_id
            
            # Check if shot timestamps reside within any of the player's on-court intervals
            for _, stint in player_stints.iterrows():
                in_time = stint['IN_TIME_REAL']
                out_time = stint['OUT_TIME_REAL']
                
                stint_condition = (df['SHOT_TIME_TENTHS'] >= in_time) & (df['SHOT_TIME_TENTHS'] <= out_time)
                df.loc[game_mask & stint_condition, 'PLAYER_ON_COURT'] = True
                
            # Polite pause to keep the NBA Stats firewall happy
            time.sleep(0.6)
            
        except Exception as e:
            print(f"Warning: Could not process rotation matrix for Game {game_id}. Error: {e}")
            
    # Apply user filtering selection
    if exclude_player:
        filtered_df = df[df['PLAYER_ON_COURT'] == False]
    else:
        filtered_df = df[df['PLAYER_ON_COURT'] == True]
        
    # Drop tracking columns before passing back clean data
    return filtered_df.drop(columns=['SHOT_TIME_TENTHS', 'PLAYER_ON_COURT'])