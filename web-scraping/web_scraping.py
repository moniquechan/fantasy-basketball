#!/usr/bin/python
import sys, getopt
from datetime import datetime, timedelta
import re
import os
from get_data import get_fantasy_data, get_game_data

def validate_date(date):
    # validate date format
    date_format = re.compile(r"[2][0][12][0-9]-[01][1-9]-[0123][0-9]")
    if re.fullmatch(date_format, date):
        return True
    else:
        return False


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
    start_date = date
    if not os.path.exists('fantasy-data'):
        os.makedirs('fantasy-data')
    if not os.path.exists('game-data'):
        os.makedirs('game-data')
    if (validate_date(date)):
        # get data for the amount of the days with option -d in command line
        for i in range(days):
            try:
                # get fantasy data
                df = get_fantasy_data(date)
                df.to_csv('./fantasy-data/' + date, index=False)
                get_game_data(date)
                date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')

            except IndexError:
                print('No data found on ' + date)
                date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
            
            print("Data saved: " + date)
    else:
        print('Not a valid date format')



