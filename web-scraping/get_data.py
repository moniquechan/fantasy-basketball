import requests
import pandas as pd
from lxml import html
import time
import os

# scraping fantasy data using requests
def get_fantasy_data(date):
        # scraping the site for fantasy player data
        r = requests.get("https://service.fantasylabs.com/contest-sources/?sport_id=2&date=" + date)
        group_id = r.json()['contest-sources'][0]['draft_groups'][0]['id']
        r = requests.get("https://service.fantasylabs.com/live-contests/?sport=NBA&contest_group_id=" + str(group_id))
        contest_id = r.json()['live_contests'][0]['contest_id']
        player_data = requests.get("https://dh5nxc6yx3kwy.cloudfront.net/contests/nba/" + date.replace('-','') +"/" + str(contest_id) + "/data/")

        # add player data to a data frame
        df = pd.DataFrame()
        for i in player_data.json()['players']:
            df_dictionary = pd.DataFrame([player_data.json()['players'][i]])
            df = pd.concat([df, df_dictionary], ignore_index=True)
        return df

def to_abbrev_team_name(team):
    teams = {
    "Atlanta Hawks": "ATL",
    "Brooklyn Nets": "BKN",
    "Boston Celtics": "BOS",
    "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL",
    "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET",
    "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU",
    "Indiana Pacers": "IND",
    "Los Angeles Clippers": "LAC",
    "LA Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN",
    "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC",
    "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA",
    "Washington Wizards": "WAS"}
    return teams[team]

    
def get_game_data(date):
    year, month, day = date.split('-')
    links = []

    stat_header = ['Date','Player','Team','MIN','FG','3PT','FT','OREB','DREB','REB','AST','STL','BLK','TO','PF','+/-','PTS']

    html_content = requests.get(f"https://www.espn.com/nba/scoreboard/_/date/{year}{month}{day}")
    dom = html.fromstring(html_content.content)

    # get boxscore game id
    ele = dom.xpath('//a[text()="Box Score"]')
    for i in ele:
        links.append(i.attrib['href'])

    # create folder for all games played on date
    if not os.path.exists('game-data/' + date) and len(links) > 0:
        os.makedirs('game-data/' + date)
    
    # get boxscore data
    players = []
    player_stats = []

    for link in links:
        html_content = requests.get(f"https://www.espn.com{link}")
        time.sleep(0.5)
        dom = html.fromstring(html_content.content)
        
        ele = dom.xpath('//div[contains(@class, "Boxscore")]/div[contains(@class, "Boxscore ")]')
        team_names =  dom.xpath('//div[contains(@class, "Boxscore__Title")]/div/text()')
        team_names[0] = to_abbrev_team_name(team_names[0])
        team_names[1] = to_abbrev_team_name(team_names[1])
        
        for section in ele:
            players.append(section.xpath('div/table/tbody/tr/td[not(contains(@class, "Table__customHeader"))]/div/a/text()'))
            player_stats.append(section.xpath('div/div/div/table/tbody/tr/td[not(contains(@class, "Table__customHeader"))]/text()'))
        
        # add data to data frame
        df = pd.DataFrame(columns=stat_header)
        for i in range(2):
            player_stats[i] = player_stats[i] + ['DNP']*((len(players[i])*14)-len(player_stats[i]))
            for j in range(len(players[i])):
                to_append = []
                index = j *14
                to_append = [date, players[i][j], team_names[i], player_stats[i][index], player_stats[i][index+1], player_stats[i][index+2],player_stats[i][index+3], 
                    player_stats[i][index+4], player_stats[i][index+5],player_stats[i][index+6],player_stats[i][index+7], player_stats[i][index+8], player_stats[i][index+9],player_stats[i][index+10], 
                    player_stats[i][index+11], player_stats[i][index+12],player_stats[i][index+13]]
                df.loc[len(df)] = to_append
        df.to_csv('./game-data/' + date + '/' + date + team_names[0]+team_names[1], index=False)
