import pandas as pd
from nba_api.stats.endpoints import shotchartdetail

def fetch_shot_data(team_id: int = 0, player_id: int = 0, opponent_id: int = 0, season: str = "2025-26", season_type: str = "Playoffs") -> pd.DataFrame:
    """Fetches raw shot chart data from the NBA API."""
    shot_data = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=player_id,
        opponent_team_id=opponent_id,
        context_measure_simple='FGA',
        season_nullable=season,
        season_type_all_star=season_type
    )
    return shot_data.get_data_frames()[0]