from nba_api.stats.endpoints._base import Endpoint
from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.library.parameters import LastNGames, MeasureTypeDetailedDefense, Month, PaceAdjust, PerModeDetailed, Period, PlusMinus, Rank, Season, SeasonTypeAllStar, ConferenceNullable, DivisionSimpleNullable, GameScopeSimpleNullable, GameSegmentNullable, LeagueIDNullable, LocationNullable, OutcomeNullable, PlayerExperienceNullable, PlayerPositionAbbreviationNullable, SeasonSegmentNullable, ShotClockRangeNullable, StarterBenchNullable, DivisionNullable, DayOffset, GameDate, LeagueID
from nba_api.stats.library.parameters import GameSegmentNullable, LastNGamesNullable, LeagueIDNullable, LocationNullable, MonthNullable, OutcomeNullable, PerModeSimpleNullable, PeriodNullable, SeasonNullable, SeasonSegmentNullable, SeasonTypeNullable, ShotClockRangeNullable, ConferenceNullable, DivisionNullable
import datetime
import random
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#scraping statistics from NBA.com
class LeagueDashTeamStats(Endpoint):
    endpoint = 'leaguedashteamstats'
    expected_data = {'LeagueDashTeamStats': ['TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 'CFID', 'CFPARAMS']}

    nba_response = None
    data_sets = None
    player_stats = None
    team_stats = None
    headers = None

    def __init__(self,
                 last_n_games=5,
                 measure_type_detailed_defense=MeasureTypeDetailedDefense.default,
                 month=Month.default,
                 opponent_team_id=0,
                 pace_adjust=PaceAdjust.default,
                 per_mode_detailed=PerModeDetailed.default,
                 period=Period.default,
                 plus_minus=PlusMinus.default,
                 rank=Rank.default,
                 season=Season.default,
                 season_type_all_star=SeasonTypeAllStar.default,
                 conference_nullable=ConferenceNullable.default,
                 date_from_nullable='',
                 date_to_nullable='',
                 division_simple_nullable=DivisionSimpleNullable.default,
                 game_scope_simple_nullable=GameScopeSimpleNullable.default,
                 game_segment_nullable=GameSegmentNullable.default,
                 league_id_nullable=LeagueIDNullable.default,
                 location_nullable=LocationNullable.default,
                 outcome_nullable=OutcomeNullable.default,
                 po_round_nullable='',
                 player_experience_nullable=PlayerExperienceNullable.default,
                 player_position_abbreviation_nullable=PlayerPositionAbbreviationNullable.default,
                 season_segment_nullable=SeasonSegmentNullable.default,
                 shot_clock_range_nullable=ShotClockRangeNullable.default,
                 starter_bench_nullable=StarterBenchNullable.default,
                 team_id_nullable='',
                 two_way_nullable='',
                 vs_conference_nullable=ConferenceNullable.default,
                 vs_division_nullable=DivisionNullable.default,
                 proxy=None,
                 headers=None,
                 timeout=30,
                 get_request=True):
        self.proxy = proxy
        if headers is not None:
            self.headers = headers
        self.timeout = timeout
        self.parameters = {
                'LastNGames': last_n_games,
                'MeasureType': measure_type_detailed_defense,
                'Month': month,
                'OpponentTeamID': opponent_team_id,
                'PaceAdjust': pace_adjust,
                'PerMode': per_mode_detailed,
                'Period': period,
                'PlusMinus': plus_minus,
                'Rank': rank,
                'Season': season,
                'SeasonType': season_type_all_star,
                'Conference': conference_nullable,
                'DateFrom': date_from_nullable,
                'DateTo': date_to_nullable,
                'Division': division_simple_nullable,
                'GameScope': game_scope_simple_nullable,
                'GameSegment': game_segment_nullable,
                'LeagueID': league_id_nullable,
                'Location': location_nullable,
                'Outcome': outcome_nullable,
                'PORound': po_round_nullable,
                'PlayerExperience': player_experience_nullable,
                'PlayerPosition': player_position_abbreviation_nullable,
                'SeasonSegment': season_segment_nullable,
                'ShotClockRange': shot_clock_range_nullable,
                'StarterBench': starter_bench_nullable,
                'TeamID': team_id_nullable,
                'TwoWay': two_way_nullable,
                'VsConference': vs_conference_nullable,
                'VsDivision': vs_division_nullable
        }
        if get_request:
            self.get_request()
    
    def get_request(self):
        self.nba_response = NBAStatsHTTP().send_api_request(
            endpoint=self.endpoint,
            parameters=self.parameters,
            proxy=self.proxy,
            headers=self.headers,
            timeout=self.timeout,
        )
        self.load_response()
        
    def load_response(self):
        data_sets = self.nba_response.get_data_sets()
        self.data_sets = [Endpoint.DataSet(data=data_set) for data_set_name, data_set in data_sets.items()]
        self.league_dash_team_stats = Endpoint.DataSet(data=data_sets['LeagueDashTeamStats'])

#scraping the scoreboard from NBA.com
class Scoreboard(Endpoint):
    endpoint = 'scoreboard'
    expected_data = {'Available': ['GAME_ID', 'PT_AVAILABLE'], 'EastConfStandingsByDay': ['TEAM_ID', 'LEAGUE_ID', 'SEASON_ID', 'STANDINGSDATE', 'CONFERENCE', 'TEAM', 'G', 'W', 'L', 'W_PCT', 'HOME_RECORD', 'ROAD_RECORD', 'RETURNTOPLAY'], 'GameHeader': ['GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 'GAME_STATUS_ID', 'GAME_STATUS_TEXT', 'GAMECODE', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'SEASON', 'LIVE_PERIOD', 'LIVE_PC_TIME', 'NATL_TV_BROADCASTER_ABBREVIATION', 'LIVE_PERIOD_TIME_BCAST', 'WH_STATUS'], 'LastMeeting': ['GAME_ID', 'LAST_GAME_ID', 'LAST_GAME_DATE_EST', 'LAST_GAME_HOME_TEAM_ID', 'LAST_GAME_HOME_TEAM_CITY', 'LAST_GAME_HOME_TEAM_NAME', 'LAST_GAME_HOME_TEAM_ABBREVIATION', 'LAST_GAME_HOME_TEAM_POINTS', 'LAST_GAME_VISITOR_TEAM_ID', 'LAST_GAME_VISITOR_TEAM_CITY', 'LAST_GAME_VISITOR_TEAM_NAME', 'LAST_GAME_VISITOR_TEAM_CITY1', 'LAST_GAME_VISITOR_TEAM_POINTS'], 'LineScore': ['GAME_DATE_EST', 'GAME_SEQUENCE', 'GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY_NAME', 'TEAM_WINS_LOSSES', 'PTS_QTR1', 'PTS_QTR2', 'PTS_QTR3', 'PTS_QTR4', 'PTS_OT1', 'PTS_OT2', 'PTS_OT3', 'PTS_OT4', 'PTS_OT5', 'PTS_OT6', 'PTS_OT7', 'PTS_OT8', 'PTS_OT9', 'PTS_OT10', 'PTS', 'FG_PCT', 'FT_PCT', 'FG3_PCT', 'AST', 'REB', 'TOV'], 'SeriesStandings': ['GAME_ID', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'GAME_DATE_EST', 'HOME_TEAM_WINS', 'HOME_TEAM_LOSSES', 'SERIES_LEADER'], 'WestConfStandingsByDay': ['TEAM_ID', 'LEAGUE_ID', 'SEASON_ID', 'STANDINGSDATE', 'CONFERENCE', 'TEAM', 'G', 'W', 'L', 'W_PCT', 'HOME_RECORD', 'ROAD_RECORD']}

    nba_response = None
    data_sets = None
    player_stats = None
    team_stats = None
    headers = None

    def __init__(self,
                 day_offset=DayOffset.default,
                 game_date=GameDate.default,
                 league_id=LeagueID.default,
                 proxy=None,
                 headers=None,
                 timeout=30,
                 get_request=True):
        self.proxy = proxy
        if headers is not None:
            self.headers = headers
        self.timeout = timeout
        self.parameters = {
                'DayOffset': day_offset,
                'GameDate': game_date,
                'LeagueID': league_id
        }
        if get_request:
            self.get_request()
    
    def get_request(self):
        self.nba_response = NBAStatsHTTP().send_api_request(
            endpoint=self.endpoint,
            parameters=self.parameters,
            proxy=self.proxy,
            headers=self.headers,
            timeout=self.timeout,
        )
        self.load_response()
        
    def load_response(self):
        data_sets = self.nba_response.get_data_sets()
        self.data_sets = [Endpoint.DataSet(data=data_set) for data_set_name, data_set in data_sets.items()]
        self.available = Endpoint.DataSet(data=data_sets['Available'])
        self.east_conf_standings_by_day = Endpoint.DataSet(data=data_sets['EastConfStandingsByDay'])
        self.game_header = Endpoint.DataSet(data=data_sets['GameHeader'])
        self.last_meeting = Endpoint.DataSet(data=data_sets['LastMeeting'])
        self.line_score = Endpoint.DataSet(data=data_sets['LineScore'])
        self.series_standings = Endpoint.DataSet(data=data_sets['SeriesStandings'])
        self.west_conf_standings_by_day = Endpoint.DataSet(data=data_sets['WestConfStandingsByDay'])

#scraping the gamelogs from NBA.com
class TeamGameLogs(Endpoint):
    endpoint = 'teamgamelogs'
    expected_data = {'TeamGameLogs': ['SEASON_YEAR', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS', 'PLUS_MINUS', 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK']}

    nba_response = None
    data_sets = None
    player_stats = None
    team_stats = None
    headers = None

    def __init__(self,
                 date_from_nullable='',
                 date_to_nullable='',
                 game_segment_nullable=GameSegmentNullable.default,
                 last_n_games_nullable=LastNGamesNullable.default,
                 league_id_nullable=LeagueIDNullable.default,
                 location_nullable=LocationNullable.default,
                 measure_type_player_game_logs_nullable='Advanced',
                 month_nullable=MonthNullable.default,
                 opp_team_id_nullable=None,
                 outcome_nullable=OutcomeNullable.default,
                 po_round_nullable='',
                 per_mode_simple_nullable=PerModeSimpleNullable.default,
                 period_nullable=PeriodNullable.default,
                 player_id_nullable='',
                 season_nullable='2021-22',
                 season_segment_nullable=SeasonSegmentNullable.default,
                 season_type_nullable=SeasonTypeNullable.default,
                 shot_clock_range_nullable=ShotClockRangeNullable.default,
                 team_id_nullable='',
                 vs_conference_nullable=ConferenceNullable.default,
                 vs_division_nullable=DivisionNullable.default,
                 proxy=None,
                 headers=None,
                 timeout=30,
                 get_request=True):
        self.proxy = proxy
        if headers is not None:
            self.headers = headers
        self.timeout = timeout
        self.parameters = {
                'DateFrom': date_from_nullable,
                'DateTo': date_to_nullable,
                'GameSegment': game_segment_nullable,
                'LastNGames': last_n_games_nullable,
                'LeagueID': league_id_nullable,
                'Location': location_nullable,
                'MeasureType': measure_type_player_game_logs_nullable,
                'Month': month_nullable,
                'OppTeamID': opp_team_id_nullable,
                'Outcome': outcome_nullable,
                'PORound': po_round_nullable,
                'PerMode': per_mode_simple_nullable,
                'Period': period_nullable,
                'PlayerID': player_id_nullable,
                'Season': season_nullable,
                'SeasonSegment': season_segment_nullable,
                'SeasonType': season_type_nullable,
                'ShotClockRange': shot_clock_range_nullable,
                'TeamID': team_id_nullable,
                'VsConference': vs_conference_nullable,
                'VsDivision': vs_division_nullable
        }
        if get_request:
            self.get_request()
    
    def get_request(self):
        self.nba_response = NBAStatsHTTP().send_api_request(
            endpoint=self.endpoint,
            parameters=self.parameters,
            proxy=self.proxy,
            headers=self.headers,
            timeout=self.timeout,
        )
        self.load_response()
        
    def load_response(self):
        data_sets = self.nba_response.get_data_sets()
        self.data_sets = [Endpoint.DataSet(data=data_set) for data_set_name, data_set in data_sets.items()]
        self.team_game_logs = Endpoint.DataSet(data=data_sets['TeamGameLogs'])


#saving the statistics to df's
LeagueTraditional = LeagueDashTeamStats(measure_type_detailed_defense='Base',per_mode_detailed='Totals').get_data_frames()[0]
LeagueAdvanced = LeagueDashTeamStats(measure_type_detailed_defense='Advanced',per_mode_detailed='PerGame').get_data_frames()[0]
LeagueOpponent = LeagueDashTeamStats(measure_type_detailed_defense='Opponent',per_mode_detailed='Totals').get_data_frames()[0]
LeagueScoreboard = Scoreboard(game_date=str(datetime.date.today())).get_data_frames()[0]

#create a df with the following columns that will pull data from the df's created above
OU_Model = pd.DataFrame(columns=['TeamID',
                                 'Team',
                                 'PTS',
                                 'OPP PTS',
                                 'POSS',
                                 'PACE',
                                 'PTS/POSS',
                                 'OPP PTS/POSS'])

#copying team id's to ou_model
OU_Model['TeamID'] = LeagueTraditional['TEAM_ID']

#calculating values in ou_model from the df's that were scraped from nba.com for each teamid
OU_Model['Team'] = LeagueTraditional['TEAM_NAME'].where(OU_Model['TeamID'] == LeagueTraditional['TEAM_ID'])
OU_Model['PTS'] = LeagueTraditional['PTS'].where(OU_Model['TeamID'] == LeagueTraditional['TEAM_ID'])
OU_Model['OPP PTS'] = LeagueOpponent['OPP_PTS'].where(OU_Model['TeamID'] == LeagueOpponent['TEAM_ID'])
OU_Model['POSS'] = LeagueAdvanced['POSS'].where(OU_Model['TeamID'] == LeagueAdvanced['TEAM_ID'])
OU_Model['PACE'] = LeagueAdvanced['PACE'].where(OU_Model['TeamID'] == LeagueAdvanced['TEAM_ID'])

OU_Model['PTS/POSS'] = OU_Model['PTS']/OU_Model['POSS']
OU_Model['OPP PTS/POSS'] = OU_Model['OPP PTS']/OU_Model['POSS']

#saving ou_model df to excel
OU_Model.to_excel(r'OU_Model.xlsx','Master Sheet')

#creating function to calculate projected o/u for the day's games
def get_todays_games(df1,df2):
    
    print('Calculating projected totals....')
    
    #set the random seed so results can be easily reproduced
    random.seed(0)
    
    #creating new df
    df3 = df1[['HOME_TEAM_ID','VISITOR_TEAM_ID']]
    
    #add the following columns to the new df
    df3['Home Pts Poss'] = ''
    df3['Home Opp Pts Poss'] = ''
    df3['Visitor Pts Poss'] = ''
    df3['Visitor Opp Pts Poss'] = ''
    df3['Proj Total'] = ''
    df3['Fan Duel Total'] = ''
    df3['Decision'] = ''
    
    df3.insert(2,'Home Team','')
    df3.insert(3,'Visitor Team','')
    
    #interate through each index position in the ou_model
    for idx in df2.index:
        item1 = df2.at[idx,'TeamID']
        team = df2.at[idx,'Team']
        pts = df2.at[idx,'PTS/POSS']
        opp_pts = df2.at[idx,'OPP PTS/POSS']
        
        #iterate through each index position in the new df
        for idx in df3.index:
            
            item2 = df3.at[idx,'HOME_TEAM_ID']
            item3 = df3.at[idx,'VISITOR_TEAM_ID']
            
            #if home_tead_id is equal to the teamid at the index position in the ou_model
            if item2 == item1:
                df3.at[idx,'Home Team'] = team
                df3.at[idx,'Home Pts Poss'] = pts
                df3.at[idx,'Home Opp Pts Poss'] = opp_pts
            #if visitor_team_id is equal to the teamid at the index position in the ou_model
            elif item3 == item1:
                df3.at[idx,'Visitor Team'] = team
                df3.at[idx,'Visitor Pts Poss'] = pts
                df3.at[idx,'Visitor Opp Pts Poss'] = opp_pts
            #if teamid is not found
            else:    
                continue
    #iterate through each index position in the new df
    for idx in df3.index:
        
        #create an empty list to store results of simulated game total
        gamescore = []
        
        #define the numnber of simulations you want to run
        ns = 1000
        
        #scrape the game logs for the home and away team from NBA.com
        home_poss = TeamGameLogs(team_id_nullable=df3.at[idx,'HOME_TEAM_ID']).get_data_frames()[0]
        vis_poss = TeamGameLogs(team_id_nullable=df3.at[idx,'VISITOR_TEAM_ID']).get_data_frames()[0]
        
        #calcuate the mean and standard deviation of possesions for both home and away in their previous 5 games
        home_poss_mean = home_poss.iloc[:5]['POSS'].mean()
        home_poss_std = home_poss.iloc[:5]['POSS'].std()
        vis_poss_mean = vis_poss.iloc[:5]['POSS'].mean()
        vis_poss_std = vis_poss.iloc[:5]['POSS'].std()                                                                                            
        
        
        #for each simulation randomly calculate home and away possesions and take the average of those two numbers
        #calcuate the score based on the number of possesions and save the score to the gamescore list                                                                                             
        for i in range(ns):                                                                                             
            poss = (random.gauss(home_poss_mean,home_poss_std) + random.gauss(vis_poss_mean,vis_poss_std))/2
            hs = poss * ((df3.at[idx,'Home Pts Poss'] + df3.at[idx,'Visitor Opp Pts Poss'])/2)
            aws = poss * ((df3.at[idx,'Visitor Pts Poss'] + df3.at[idx,'Home Opp Pts Poss'])/2)
            score = hs + aws
            gamescore.append(score)
        
        #save the average of the 1000 gamescores calculated to the Proj Total column
        df3.at[idx,'Proj Total'] = (sum(gamescore)/len(gamescore))
    
    #iterate through each index position of the new df
    for idx in df3.index:
        
        #input the total per fan duel for each matchup
        df3.at[idx,'Fan Duel Total'] = float(input('{} @ {}  '.format(df3.at[idx,'Visitor Team'],df3.at[idx,'Home Team'])))
    
    #iterate through each index position of thew new df
    for idx in df3.index:
        
        #if the proj total of the matchup < fan duel total = bet the under, if not bet the over
        if df3.at[idx,'Proj Total'] < df3.at[idx,'Fan Duel Total']:
            df3.at[idx,'Decision'] = 'Under'
        else:
            df3.at[idx,'Decision'] = 'Over'
    
    #display the columns below after the the decisions are made        
    pd.set_option('display.max_columns',None)
    pd.set_option('display.width',1000)
    print(df3[['Home Team','Visitor Team','Proj Total','Fan Duel Total','Decision']])

#pass leaguescoreboard and ou_model through the function
get_todays_games(LeagueScoreboard,OU_Model)

#print model has been updated successfully
print('Model Updated Successfully!')








