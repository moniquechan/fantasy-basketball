# Fantasy Basketball Web Scraping, Data Analysis, and Prediction

This project is uses a python script that scrapes data from a site called [rotogrinders](https://rotogrinders.com/resultsdb/nba) that contains information on the Daily Fantasy stats for the NBA.

#### Project Status: [In Progress]

## Getting Started

Follow the instructions to get a copy of the project up and running on your local machine


### Installing


Install the requirements of the project by running the command in the root directory

```
pip install -r requirements.txt
```

The project should be ready to run after the installation

## Running the Project

### Web Scraping
This project scrapes data from [rotogrinders](https://rotogrinders.com/resultsdb/nba) for information on the Daily NBA Fantasy stats provided by [Draft Kings](https://www.draftkings.com/) and box score data from [ESPN](https://www.espn.com/nba/scoreboard).

In the path `fantasy-basketball/web-scraping` we can run our python file with the format: 
```
python  web_scraping.py [date] [-d numberOfDays]
```

This command will extract from [rotogrinders](https://rotogrinders.com/resultsdb/nba) and [ESPN](https://www.espn.com/nba/scoreboard) for their respective data. The `date` must be in the format `yyyy-mm-dd`. If the `-d` option is supplied, the script will run for `numberOfDays` times for the preceeding days of the date that was given.

#### Sample Dataset
`fantasy-basketball/web-scraping/fantasy-data/2022-11-01.csv`
|playerId|firstName   |lastName|fullName          |salary|position|rosterPosition|currentTeam|currentTeamId|eventId|eventTeamId|homeVisitor|favDog  |projPoints|ownership|actualPoints|statDetails|madeCut|Date      |
|--------|------------|--------|------------------|------|--------|--------------|-----------|-------------|-------|-----------|-----------|--------|----------|---------|------------|-----------|-------|----------|
|12012   |Chris       |Paul    |Chris Paul        |7700  |PG      |PG            |PHX        |2024         |5402170|54021702   |Home       |Favorite|38.61     |10.58    |50.5        |           |0      |2022-11-01|
|12060   |D'Angelo    |Russell |D'Angelo Russell  |7000  |PG      |PG            |MIN        |2065         |5402170|54021701   |Visitor    |Dog     |30.56     |8.16     |14.5        |           |0      |2022-11-01|
|12061   |Karl-Anthony|Towns   |Karl-Anthony Towns|8800  |C       |PF/C          |MIN        |2065         |5402170|54021701   |Visitor    |Dog     |42.59     |9.39     |50.0        |           |0      |2022-11-01|

`fantasy-basketball/web-scraping/game-data/2022-11-01/2022-11-01ORLOKC.csv`
|Date |Player      |Team   |MIN               |FG   |3PT|FT   |OREB|DREB|REB    |AST     |STL    |BLK     |TO   |PF   |+/-  |PTS|
|-----|------------|-------|------------------|-----|---|-----|----|----|-------|--------|-------|--------|-----|-----|-----|---|
|2022-11-01|P. Banchero |ORL    |37                |6-13 |0-1|3-3  |0   |8   |8      |2       |1      |0       |4    |0    |+1   |15 |
|2022-11-01|F. Wagner   |ORL    |37                |8-18 |1-5|3-3  |0   |1   |1      |7       |1      |2       |2    |2    |+12  |20 |
|2022-11-01|W. Carter Jr.|ORL    |35                |10-15|2-2|8-8  |5   |7   |12     |2       |2      |1       |2    |3    |+4   |30 |


### Data Cleaning

Open the Juypter Notebook file for data cleaning located in `fantasy-basketball/data-cleaning/`
```
jupyter notebook cleaning.ipynb
```

Running the notebook will clean the data from `fantasy-basketball/web-scraping/game-data` and `fantasy-basketball/web-scraping/fantasy-data` and will output 3 files:

`clean-data.csv`
|fullName        |salary|position|projPoints|ownership|actualPoints|Date      |Team|MIN|OREB|DREB|REB|AST|STL|BLK|TO |PF |+/-|PTS|FGA|FGM|3PTA|3PTM|FTA|FTM|
|----------------|------|--------|----------|---------|------------|----------|----|---|----|----|---|---|---|---|---|---|---|---|---|---|----|----|---|---|
|Chris Paul      |7700  |PG      |38.61     |10.58    |50.5        |2022-11-01|PHX |34 |1   |7   |8  |12 |3  |0  |1  |2  |18 |15 |5  |12 |1   |5   |4  |6  |
|D'Angelo Russell|7000  |PG      |30.56     |8.16     |14.5        |2022-11-01|MIN |23 |0   |4   |4  |4  |0  |0  |4  |3  |-20|5  |2  |8  |1   |3   |0  |0  |
|Karl-Anthony Towns|8800  |C       |42.59     |9.39     |50.0        |2022-11-01|MIN |37 |5   |5   |10 |7  |0  |1  |4  |4  |-12|24 |9  |18 |3   |7   |3  |3  |

`fantasy-table.csv`
|firstName       |lastName|fullName|salary|position|currentTeam|projPoints|ownership|actualPoints|Date|initialName|
|----------------|--------|--------|------|--------|-----------|----------|---------|------------|----|-----------|
|Chris           |Paul    |Chris Paul|7700  |PG      |PHX        |38.61     |10.58    |50.5        |2022-11-01|C. Paul    |
|D'Angelo        |Russell |D'Angelo Russell|7000  |PG      |MIN        |30.56     |8.16     |14.5        |2022-11-01|D. Russell |
|Karl-Anthony    |Towns   |Karl-Anthony Towns|8800  |C       |MIN        |42.59     |9.39     |50.0        |2022-11-01|K. Towns   |

`game-table.csv`
|Date            |Player|Team|MIN  |OREB |DREB|REB       |AST|STL|BLK|TO |PF |+/-|PTS|FGA|FGM|3PTA|3PTM|FTA|FTM|
|----------------|------|----|-----|-----|----|----------|---|---|---|---|---|---|---|---|---|----|----|---|---|
|2022-11-01      |P. Williams|CHI |30   |3    |4   |7         |1  |1  |2  |3  |2  |-8 |12 |5  |10 |0   |3   |2  |2  |
|2022-11-01      |D. DeRozan|CHI |33   |0    |4   |4         |1  |3  |0  |1  |2  |-1 |20 |8  |21 |1   |2   |3  |3  |
|2022-11-01      |N. Vucevic|CHI |32   |3    |12  |15        |2  |1  |0  |1  |2  |+5 |7  |3  |8  |0   |1   |1  |2  |

### Data Visualization

The Power BI dashboard displays the fantasy information on specific players and teams which can be found [here](https://github.com/moniquechan/fantasy-basketball/blob/main/data-analysis/analysis/FantasyDashboard.pbix)

When a team is selected as a filter the dashboard, the cards on the top right will show the average fantasy points, projected fantasy points, and salary over all game dates the team played in. 

The projected and actual fantasy points accumulated by the team is displayed on the graph on the bottom left. Looking at this graph we can see if a team over achieved or under achieved after each day by comparing the bars and the line.
![Team Dashboard Screenshot](./data-analysis/analysis/screenshots/TeamDashboard.PNG)

A player can be selected in the filter to see more detailed infomation for a single player. Similar to the team dashboard, the graph displays the selected player's projected and actual fantasy points.

The graph on the bottom right displays the performance of the player for each game their team played in.

![Player Dashboard Screenshot](./data-analysis/analysis/screenshots/PlayerDashboard.PNG)

The Fantasy dashboard uses `clean-data.csv` as the data for all the visuals.

## Technologies

* [Python](https://www.python.org/) - Web Scraping, Data Cleaning
* [Power BI](https://powerbi.microsoft.com/en-us/) - Data Visualization


## Authors

* **Monique Chan** - *Initial work* - [github](https://github.com/moniquechan)

