import pandas as pd
from nba_api.stats.endpoints import shotchartdetail

def fetch_player_shot_data(player_id: int, season: str = "2025-26", season_type: str = "Playoffs") -> pd.DataFrame:
    """Fetches raw shot chart data from the NBA API."""
    shot_data = shotchartdetail.ShotChartDetail(
        team_id=0,
        player_id=player_id,
        context_measure_simple='FGA',
        season_nullable=season,
        season_type_all_star=season_type
    )
    return shot_data.get_data_frames()[0]