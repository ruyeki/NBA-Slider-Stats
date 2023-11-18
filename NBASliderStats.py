import streamlit as st
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.static import players
import pandas as pd


def get_player_season_totals(active_player_ids):
    year = '2023-24'
    season = leaguedashplayerstats.LeagueDashPlayerStats(season=year)
    season_totals_regular_season = season.get_data_frames()[0]  # Get the SeasonTotalsRegularSeason dataframe
    season_totals_active_players = season_totals_regular_season[season_totals_regular_season['PLAYER_ID'].isin(active_player_ids)]
    filtered_season_totals = season_totals_active_players[columns_to_keep]
    return filtered_season_totals

if __name__ == "__main__":
    columns_to_keep = [
            "PLAYER_ID",
            "PLAYER_NAME",
            "AGE",
            "GP",
            "W",
            "L",
            "W_PCT",
            "MIN",
            "FGM",
            "FGA",
            "FG_PCT",
            "FG3M",
            "FG3A",
            "FG3_PCT",
            "FTM",
            "FTA",
            "FT_PCT",
            "OREB",
            "DREB",
            "REB",
            "AST",
            "TOV",
            "STL",
            "BLK",
            "BLKA",
            "PF",
            "PFD",
            "PTS",
            "PLUS_MINUS",
            "DD2",
            "TD3",
    
]

    st.title('NBA Player Season Totals (Regular Season)')
    
    active_players_data = players.get_active_players()
    active_player_ids = [player['id'] for player in active_players_data]
    season_totals_active_players = get_player_season_totals(active_player_ids)

    st.sidebar.title('Rank Stats')

    # Create sliders for each stat
    sliders = {}
    for stat in columns_to_keep:
        sliders[stat] = st.sidebar.slider(f'Importance of {stat}', 0.0, 1.0, 0.5, 0.1)

    # Calculate weighted sum based on user-defined importance
    weights = pd.Series(sliders)
    normalized_weights = weights / weights.sum()

    # Multiply each column by its weight and sum across columns
    weighted_totals = season_totals_active_players[columns_to_keep].mul(normalized_weights)
    season_totals_active_players['Weighted_Sum'] = weighted_totals.sum(axis=1)

    # Display sorted players based on weighted sum
    sorted_players = season_totals_active_players.sort_values(by='Weighted_Sum', ascending=False)

    
    st.write("Season Totals (Regular Season) for Active NBA Players:")
    st.write(sorted_players)