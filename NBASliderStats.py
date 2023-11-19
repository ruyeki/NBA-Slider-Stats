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

def calculate_per_game_stats(data):
    #calculates per game cause i don't think it's avaialble for the nba_api?? or i might be blind
    data['PTS '] = data['PTS'] / data['GP']
    data['REB '] = data['REB'] / data['GP']
    data['FGM '] = data['FGM'] / data['GP']
    data['FGA '] = data['FGA'] / data['GP']
    data['FG3M '] = data['FG3M'] / data['GP']
    data['FG3A '] = data['FG3A'] / data['GP']
    data['FTM '] = data['FTM'] / data['GP']
    data['FTA '] = data['FTA'] / data['GP']
    data['PLUS_MINUS '] = data['PLUS_MINUS'] / data['GP']
    data['PFD '] = data['PFD'] / data['GP']
    data['PF '] = data['PF'] / data['GP']
    data['OREB '] = data['OREB'] / data['GP']
    data['DREB '] = data['DREB'] / data['GP']
    data['AST '] = data['AST'] / data['GP']
    data['TOV '] = data['TOV'] / data['GP']
    data['STL '] = data['STL'] / data['GP']
    data['BLK '] = data['BLK'] / data['GP']
    data['BLKA '] = data['BLKA'] / data['GP']
    data['MIN '] = data['MIN'] / data['GP']

    data = data[columns_to_keepPG]

    return data

if __name__ == "__main__":
    #Removing unneccessary columns
    columns_to_keep = [
    "PLAYER_NAME", "AGE", "GP", "W", "L", "W_PCT", "MIN", "FGM", "FGA", "FG_PCT",
    "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "OREB", "DREB", "REB",
    "AST", "TOV", "STL", "BLK", "BLKA", "PF", "PFD", "PTS", "PLUS_MINUS", "DD2", "TD3"
    ]
    #Added a space in every category to ensure it wouldn't get confuse when using both the Season total and per game stats
    columns_to_keepPG = [
    "PLAYER_NAME", "MIN ", "FGM ", "FGA ",
    "FG3M ", "FG3A ", "FTM ", "FTA ", "OREB ", "DREB ", "REB ",
    "AST ", "TOV ", "STL ", "BLK ", "BLKA ", "PF ", "PFD ", "PTS ", "PLUS_MINUS ",
]



    st.title('NBA Player Season Totals (Regular Season)')
    #allows user to choose a year going back to earlier they have which is 1997??? don't know why
    available_years = [f"{year}-{str(year+1)[-2:]}" for year in range(2023, 1995, -1)]  # Adjust the range as needed
    selected_year = st.sidebar.selectbox('Select a Year', available_years)

    #Need to change the variable names because it says active right now but i have it 
    #set to all nba players at the moment
    #We need options for filters which sounds like a lot of busy work like "only show ppg 
    #above 20 or only show GP above 30 or active players only" 
    active_players_data = players.get_players()
    active_player_ids = [player['id'] for player in active_players_data]

    #Throughout this whole rest i have same lines for both season total and season per game
    season_totals_active_players = get_player_season_totals(active_player_ids, selected_year)
    season_perGame_active_players = calculate_per_game_stats(season_totals_active_players.copy())

    st.sidebar.title('Rank Stats')
    #Excludes player name
    selected_stats = st.sidebar.multiselect('Select Total Stats to Rank', [col for col in columns_to_keep if col != 'PLAYER_NAME'])

    # Create sliders for importance
    sliders = {}
    for stat in selected_stats:
        sliders[stat] = st.sidebar.slider(f'Importance of {stat}', 0.0, 1.0, 0.5, 0.01)
    
    selectedPG_stats = st.sidebar.multiselect('Select Per Game Stats to Rank', [col for col in columns_to_keepPG if col != 'PLAYER_NAME'])
    slidersPG = {}
    for stat in selectedPG_stats:
        slidersPG[stat] = st.sidebar.slider(f'Importance of {stat}', 0.0, 1.0, 0.5, 0.01)

    # Filter the DataFrame based on selected stats
    filtered_data = season_totals_active_players[selected_stats]
    filtered_dataPG = season_perGame_active_players[selectedPG_stats]
    # Calculate weighted sum based on user-defined importance
    normalized_data = (filtered_data - filtered_data.min()) / (filtered_data.max() - filtered_data.min())
    normalized_dataPG = (filtered_dataPG - filtered_dataPG.min()) / (filtered_dataPG.max() - filtered_dataPG.min())
    # Calculate weighted sum based on user-defined importance
    weighted_totals = normalized_data * pd.Series(sliders)
    weighted_totalsPG = normalized_dataPG * pd.Series(slidersPG)
    # Calculate the total weighted sum for each player
    season_totals_active_players['Weighted_Sum'] = weighted_totals.sum(axis=1) + weighted_totalsPG.sum(axis=1)
    season_perGame_active_players['Weighted_Sum'] = weighted_totals.sum(axis=1) + weighted_totalsPG.sum(axis=1)
    # Display sorted players based on weighted sum
    sorted_players = season_totals_active_players.sort_values(by='Weighted_Sum', ascending=False)
    
    sorted_playersPG = season_perGame_active_players.sort_values(by='Weighted_Sum', ascending=False)

    st.write("Season Total Stats (Regular Season) for Active NBA Players:")
    st.write(sorted_players)

    st.write("Season Per Game Stats (Regular Season) for Active NBA Players:")
    st.write(sorted_playersPG)

