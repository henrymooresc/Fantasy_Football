import pandas as pd # Python's data munging library
from bs4 import BeautifulSoup as BS # Python's web scraping library
import requests # Python's library for making HTTP requests
from matplotlib import pyplot as plt # for visualizing the data
import seaborn as sns # for styling the visualizations
import numpy as np # for doing some maths

BASE_URL = "https://www.pro-football-reference.com/play-index/pgl_finder.cgi?request=1&match=game&year_min={season}&year_max={season}&season_start=1&season_end=-1&pos%5B%5D=QB&pos%5B%5D=WR&pos%5B%5D=RB&pos%5B%5D=TE&pos%5B%5D=OL&pos%5B%5D=DL&pos%5B%5D=LB&pos%5B%5D=DB&is_starter=E&game_type=R&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&c1stat=rush_att&c1comp=gt&c1val=0&c2stat=targets&c2comp=gt&c2val=0&c5val=1.0&order_by=rush_yds&offset={offset}"

def get_weekly_stats(season=2020, week=1):

    offset = 0 # start on the first page

    df = pd.DataFrame() # intstantiate an empty DataFrame

    while True:

        URL = BASE_URL.format(season=season, week=week, offset=offset) # format our URL with the updated offset

        res = requests.get(URL) # make a HTTP requests to pfr to get the HTML content

        soup = BS(res.content, 'html.parser') # load the HTML content in to our web scraper

        table = soup.find('table', {'id': 'results'}) # find the table in the HTML with the id of results

        new_df = pd.read_html(str(table))[0] # read_html gets us back a list of DataFrames, get back the first and only DataFrame

        new_df.columns = new_df.columns.droplevel(level=0) # drop the first multi-column level

        # if we get back an empty DataFrame, break this loop. This means we've reached the end of our rows
        if new_df.shape[0] == 0: 
            break

        offset+=100 # increment the offset by 100 to flip to the next page

        df = pd.concat([df, new_df]) # concat this new DataFrame in to our final

    for column in df.columns: # remove unnecessary columns
        if 'Unnamed' in column:
            df = df.drop(column, axis=1)

    # Yds exists twice. The first iteration of Yds is our RushingYds, and the second is out ReceivingYds. This happened because our original df had a multi-column index.
    df['RushingYds'] = df['Yds'].iloc[:, 0] 
    df['ReceivingYds'] = df['Yds'].iloc[:, 1]

    # Same thing for TDs
    df['RushingTD'] = df['TD'].iloc[:, 0]
    df['ReceivingTD'] = df['TD'].iloc[:, 1]

    # drop unneccessary columns
    df = df.drop(['Rk', 'Yds', 'TD', 'Lg', 'Ctch%', 'Age', 'Date', 'Opp', 'Result', 'G#', 'Week', 'Day'], axis=1)

    # remove filler rows put there by PFR
    df = df.loc[df['Att'] != 'Att']

    for column in df.columns[3:]:
        df[column] = df[column].astype(np.number) # format all numeric columns as numbers

    return df

df = get_weekly_stats()

print(df.head())