#!/usr/bin/python
import sys, getopt
from datetime import datetime, timedelta
import re
import requests
import pandas as pd
import os

def validate_date(date):
    # validate date format
    date_format = re.compile(r"[2][0][12][0-9]-[01][1-9]-[0123][0-9]")
    if re.fullmatch(date_format, date):
        return True
    else:
        return False

def get_data_by_date(date):
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

try:
    if len(sys.argv) < 2:
        print('Invalid amount of Arguments')
    else:
        # command line options
        opts, args = getopt.getopt(sys.argv[2:],"d:")
        days = 1
        for opt, arg in opts:
            if opt in ['-d']:
                days = int(arg)
        
        # save data as csv
        date = sys.argv[1]
        if not os.path.exists('player-data'):
            os.makedirs('player-data')
        if (validate_date(date)):
            for i in range(days):
                df = get_data_by_date(date)
                df.to_csv('./player-data/' + date, index=False)
                date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
            print("Data saved")
        else:
            print('Not a valid date format')
except IndexError:
    print('No data found on ' + date)


