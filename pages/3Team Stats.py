import streamlit as st
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import playerestimatedmetrics
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.endpoints import scoreboardv2
import pandas as pd

def get_player_season_totals(active_player_ids, selected_year, position):
    year = selected_year
    # Add position filtering as a parameter
    season = leaguedashplayerstats.LeagueDashPlayerStats(season=year, player_position_abbreviation_nullable=position)
    season_totals_regular_season = season.get_data_frames()[0]  # Get the SeasonTotalsRegularSeason dataframe
    season_totals_active_players = season_totals_regular_season[season_totals_regular_season['PLAYER_ID'].isin(active_player_ids)]
    filtered_season_totals = season_totals_active_players[columns_to_keep]
    return filtered_season_totals

#For team stats section
def team_stats_df(selected_year):
    year = selected_year
    season_teams_stats = leaguedashteamstats.LeagueDashTeamStats(season = year)
    season_teams_df = season_teams_stats.get_data_frames()[0]
    filtered_team_frame = season_teams_df[columns_to_keepTeam]
    return filtered_team_frame
    
#For advanced stats section
def advanced_stats_df(active_player_ids, selected_year, position):
    advanced_player_stats = playerestimatedmetrics.PlayerEstimatedMetrics(season=selected_year)
    data_frame = advanced_player_stats.get_data_frames()[0]
    active_data_frame = data_frame[data_frame['PLAYER_ID'].isin(active_player_ids)]
    filtered_data_frame_adv = active_data_frame[columns_to_keepAdv]
    return filtered_data_frame_adv

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

    st.title('NBA Player Stats (Regular Season)')

    # Allows the user to choose a year going back to earlier they have, which is 1997??? don't know why
    available_years = [f"{year}-{str(year+1)[-2:]}" for year in range(2023, 1995, -1)]  # Adjust the range as needed
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
    
    
    season_teams = team_stats_df(selected_year)

    # Sidebar options based on the selected tab
    st.sidebar.title('Choose Stats')

    # Title for selecting the team stats
    st.sidebar.write("### Team Stats")
    #CHECK THIS PART
    selected_team_stats = st.sidebar.multiselect('Select Team Stats to Rank', [col for col in columns_to_keepTeam if col != 'TEAM_NAME'])

    


    # Create filter dictionaries for team stats
    filtered_data_teams = filtered_dictionary(season_teams)



    # Sidebar option for dropping unused stats
    drop_unused_stats = st.sidebar.checkbox("Drop unused stats", False)

    # Filter the DataFrame based on selected stats
    st.sidebar.title('Rank Stats')
    selected_stats = []
    sliders = {}
    sliders_filter = {}

    

    for stat in selected_team_stats:
        sliders[stat] = st.sidebar.slider(f'Importance of {stat}', -1.0, 1.0, 0.5, 0.01)
    st.sidebar.title("Range of Stats")
    for stat in selected_team_stats:
        if stat in filtered_data_teams:
            # Had to do it this way because team stats are kept as int64 and not floats
            sliders_filter[stat] = st.sidebar.slider(f'Range of {stat}', 
                                    float(filtered_data_teams[stat][0]), 
                                    float(filtered_data_teams[stat][1]),
                                    (float(filtered_data_teams[stat][0]), 
                                    float(filtered_data_teams[stat][1])))

    filtered_df = season_teams.copy()
    for col in season_teams.columns[1:]:
        if col in sliders_filter:
            filtered_df = filtered_df[filtered_df[col].between(*sliders_filter[col])]
        
    season_teams = filtered_df

    # Filter the DataFrame based on selected stats
    filtered_data = season_teams[selected_team_stats]
        
    # Normalize the data
    normalized_dataTeams = (filtered_data - filtered_data.min()) / (filtered_data.max() - filtered_data.min())
    # Calculate weighted sum based on user-defined importance
    weighted_totalsTeams = normalized_dataTeams * pd.Series(sliders)

    # Calculate the total weighted sum for each player
    season_teams['Weighted_Sum'] = weighted_totalsTeams.sum(axis=1)
    # Display sorted teams based on weighted sum
    sorted_teams = season_teams.sort_values(by=['Weighted_Sum', 'TEAM_NAME'], ascending=[False, True])
    
    if drop_unused_stats:
        sorted_teams = pd.concat([sorted_teams['TEAM_NAME'], sorted_teams[selected_team_stats], sorted_teams['Weighted_Sum']], axis = 1)

    
    st.write("Season Total Stats (Regular Season) for NBA Teams:")
    st.write(sorted_teams)
    

