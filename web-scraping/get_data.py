import requests
import pandas as pd

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