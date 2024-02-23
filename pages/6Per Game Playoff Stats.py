import streamlit as st
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import playerestimatedmetrics
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.endpoints import leaguehustlestatsplayer
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.endpoints import scoreboardv2
import pandas as pd

def get_player_season_totals(active_player_ids, selected_year, position):
    year = selected_year
    # Add position filtering as a parameter
    season = leaguedashplayerstats.LeagueDashPlayerStats(season=year, player_position_abbreviation_nullable=position, season_type_all_star='Playoffs')
    season_totals_regular_season = season.get_data_frames()[0]  # Get the SeasonTotalsRegularSeason dataframe
    season_totals_active_players = season_totals_regular_season[season_totals_regular_season['PLAYER_ID'].isin(active_player_ids)]
    filtered_season_totals = season_totals_active_players[columns_to_keep]
    return filtered_season_totals

def hustle_stats_df(active_player_ids, selected_year, position):
    hustle_player_stats = leaguehustlestatsplayer.LeagueHustleStatsPlayer(season=selected_year, player_position_nullable=position, per_mode_time = 'PerGame' ,season_type_all_star='Playoffs')
    data_frame = hustle_player_stats.get_data_frames()[0]
    active_data_frame = data_frame[data_frame['PLAYER_ID'].isin(active_player_ids)]
    filtered_data_frame_hustle = active_data_frame[columns_to_keepHustle]
    return filtered_data_frame_hustle

# Create min max dictionary of a dataframe
def filtered_dictionary(data_frame):
    filtered = {}
    for category in data_frame.columns:
        if category != 'PLAYER_NAME': # Player and Team Name does not have a "range"
            filtered[category] = [data_frame[category].min(), data_frame[category].max()]
    return filtered

def calculate_per_game_stats(data):
    # calculates per game cause I don't think it's available for the nba_api?? or I might be blind
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
    data['DD2 '] = data['DD2'] / data['GP']
    data['TD3 '] = data['TD3'] / data['GP']
    data = data[columns_to_keepPG]
    return data

if __name__ == "__main__":
    #Removing unneccessary columns
    columns_to_keep = [
        "PLAYER_NAME", "AGE","PTS","MIN", "GP", "W", "L", "W_PCT", "FGM", "FGA", "FG_PCT",
        "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "OREB", "DREB", "REB",
        "AST", "TOV", "STL", "BLK", "BLKA", "PF", "PFD", "PLUS_MINUS", "DD2", "TD3",
        "NBA_FANTASY_PTS"
    ]

    # Added a space in every category to ensure it wouldn't get confused when using both the Season total and per game stats
    columns_to_keepPG = [
        "PLAYER_NAME", "AGE", "PTS ", "MIN ", "GP", "W", "L", "W_PCT", "FGM ", "FGA ", "FG_PCT",
        "FG3M ", "FG3A ", "FG3_PCT","FTM ", "FTA ","FT_PCT", "OREB ", "DREB ", "REB ",
        "AST ", "TOV ", "STL ", "BLK ", "BLKA ", "PF ", "PFD ", "PLUS_MINUS ","DD2 ", "TD3 ",
    ]
    
    columns_to_keepTeam = [
            "TEAM_NAME",
            "W",
            "L",
            "W_PCT",
            "PTS",
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
            "PLUS_MINUS",
    ]
    
    #For advanced stats
    columns_to_keepAdv = [
            "E_OFF_RATING",
            "E_DEF_RATING",
            "E_NET_RATING",
            "E_AST_RATIO",
            "E_OREB_PCT",
            "E_DREB_PCT",
            "E_REB_PCT",
            "E_TOV_PCT",
            "E_USG_PCT"
    ]

    columns_to_keepHustle = [
            "CONTESTED_SHOTS",
            "CONTESTED_SHOTS_2PT",
            "CONTESTED_SHOTS_3PT",
            "DEFLECTIONS",
            "CHARGES_DRAWN",
            "SCREEN_ASSISTS",
            "SCREEN_AST_PTS",
            "OFF_LOOSE_BALLS_RECOVERED",
            "DEF_LOOSE_BALLS_RECOVERED",
            "LOOSE_BALLS_RECOVERED",
            "PCT_LOOSE_BALLS_RECOVERED_OFF",
            "PCT_LOOSE_BALLS_RECOVERED_DEF",
            "OFF_BOXOUTS",
            "DEF_BOXOUTS",
            "BOX_OUT_PLAYER_TEAM_REBS",
            "BOX_OUT_PLAYER_REBS",
            "BOX_OUTS",
            "PCT_BOX_OUTS_OFF",
            "PCT_BOX_OUTS_DEF",
            "PCT_BOX_OUTS_TEAM_REB",
            "PCT_BOX_OUTS_REB"
        ]

    st.title('NBA Player Stats (Regular Season)')

    # Allows the user to choose a year going back to earlier they have, which is 1997??? don't know why
    available_years = [f"{year}-{str(year+1)[-2:]}" for year in range(2022, 1995, -1)]  # Adjust the range as needed
    selected_year = st.sidebar.selectbox('Select a Year', available_years)

   # Add positions filtering
    st.sidebar.title('Select Position')
    selected_position = st.sidebar.radio('Position', ('Any Position','G', 'F', 'C'))

    #Case for if all positions are wanted
    if 'Any Position' in selected_position:
        selected_position = []
    

    # Need to change the variable names because it says active right now but I have it
    # set to all NBA players at the moment
    # We need options for filters which sounds like a lot of busy work like "only show ppg
    # above 20 or only show GP above 30 or active players only"
    active_players_data = players.get_players()
    active_player_ids = [player['id'] for player in active_players_data]
    
 
    season_perGame_active_players = calculate_per_game_stats(get_player_season_totals(active_player_ids, selected_year, selected_position))
    hustle_stats_active_players = hustle_stats_df(active_player_ids, selected_year, selected_position)

    season_perGame_active_players = [season_perGame_active_players, hustle_stats_active_players]
    season_perGame_active_players = pd.concat(season_perGame_active_players, axis=1)

    season_perGame_active_players = season_perGame_active_players.loc[:,~season_perGame_active_players.columns.duplicated()] 
    # Sidebar options based on the selected tab
    st.sidebar.title('Choose Stats')

    st.sidebar.write("### Per Game Stats")
    selected_stats_per_game = st.sidebar.multiselect('Select Per Game Stats to Rank', [col for col in columns_to_keepPG + columns_to_keepHustle if col != 'PLAYER_NAME'])

    


    # Create filter dictionaries for per game stats
    filtered_data_perGame = filtered_dictionary(season_perGame_active_players)

    # Sidebar option for dropping unused stats
    drop_unused_stats = st.sidebar.checkbox("Drop unused stats", False)

    # Filter the DataFrame based on selected stats
    st.sidebar.title('Rank Stats')
    selected_stats = []
    sliders = {}
    sliders_filter = {}

    
    for stat in selected_stats_per_game:
        sliders[stat] = st.sidebar.slider(f'Importance of {stat}', -1.0, 1.0, 0.5, 0.01)
    st.sidebar.title("Range of Stats")
    for stat in selected_stats_per_game:
        if stat in filtered_data_perGame:
            sliders_filter[stat] = st.sidebar.slider(f'Range of {stat}', 
                                    float(filtered_data_perGame[stat][0]), 
                                    float(filtered_data_perGame[stat][1]), 
                                    (float(filtered_data_perGame[stat][0]), 
                                    float(filtered_data_perGame[stat][1])))

                
                

    # Exclude all of the rows that are not in the player's range
    filtered_df = season_perGame_active_players.copy()
    for col in season_perGame_active_players.columns[1:]:
        if col in sliders_filter:
            filtered_df = filtered_df[filtered_df[col].between(*sliders_filter[col])]
        
    season_perGame_active_players = filtered_df

    # Filter the DataFrame based on selected stats
    filtered_data = season_perGame_active_players[selected_stats_per_game]
        

    # Calculate weighted sum based on user-defined importance
    normalized_dataPG = (filtered_data - filtered_data.min()) / (filtered_data.max() - filtered_data.min())
    # Calculate weighted sum based on user-defined importance
    weighted_totalsPG = normalized_dataPG * pd.Series(sliders)

    # Rounding for all per game stats
    season_perGame_active_players[columns_to_keepPG] = season_perGame_active_players[columns_to_keepPG].round(decimals=2)

    # Calculate the total weighted sum for each player
    season_perGame_active_players['Weighted_Sum'] = weighted_totalsPG.sum(axis=1)
    # Display sorted players based on weighted sum
    sorted_playersPG = season_perGame_active_players.sort_values(by=['Weighted_Sum', 'PLAYER_NAME'], ascending=[False, True])
    
    if drop_unused_stats: 
        sorted_playersPG = pd.concat([sorted_playersPG['PLAYER_NAME'], sorted_playersPG[selected_stats_per_game], sorted_playersPG['Weighted_Sum']], axis = 1)

    st.write("Season Per Game Stats (Regular Season) for Active NBA Players:")
    st.write(sorted_playersPG)  
