import pandas as pd # Python's data munging library
from bs4 import BeautifulSoup as BS # Python's web scraping library
import requests # Python's library for making HTTP requests
from matplotlib import pyplot as plt # for visualizing the data
import seaborn as sns # for styling the visualizations
import numpy as np # for doing some maths

FD = {
    'base': 'https://fantasydata.com/nfl/fantasy-football-leaders?position={pos}&season={year}&seasontype=1&scope=2&subscope=1&scoringsystem=2&startweek={week}&endweek={week}&aggregatescope=1&range=3',
    'pos': {1: 'All Offense', 2: 'QB', 3: 'RB', 4: 'WR', 5: 'TE', 6: 'K', 7: 'D/ST'}
}

def get_choices() -> list:
    # runs through possible choices for urls, returns the formatted string
    print('Choose a position by its number')
    for key in FD['pos']:
        print('{key}. {value}'.format(key=key, value=FD['pos'][key]))
    
    pos_choice = int(input('Enter num: '))

    game_choice = input('Enter a season year and week number (i.e. 2019 3): ')
    date = game_choice.split(' ')

    url_string = FD['base'].format(pos=pos_choice, year=int(date[0]), week=int(date[1]))

    return [pos_choice, date, url_string]

def pull_from_pfr(url: str) -> pd.DataFrame:
    response = requests.get(url)
    soup = BS(response.content, 'html.parser')
    table = soup.find('table', attrs={'id': 'stats_grid'})

    df = pd.read_html(str(table))[0]

    return df

def main():
    choices_list = get_choices()

    df = pull_from_pfr(choices_list[-1])

    print(df.head(15))

main()