import pandas as pd # Python's data munging library
from bs4 import BeautifulSoup as BS # Python's web scraping library
import requests # Python's library for making HTTP requests
from matplotlib import pyplot as plt # for visualizing the data
import seaborn as sns # for styling the visualizations
import numpy as np # for doing some maths

PFR = {
    'base': 'https://stathead.com/football/pgl_finder.cgi?request=1&match=game&year_min={year}&year_max={year}&season_start=1&season_end=-1&age_min=0&age_max=99&game_type=A&league_id=&team_id=&opp_id=&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&game_day_of_week=&game_location=&game_result=&handedness=&is_active=&is_hof=&c1stat={opt[0]}&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by={opt[1]}&from_link=1',
    'pos': {'QB': ['pass_att', 'pass_rating'], 'RB': ['rush_att', 'rush_yds'], 'WR': ['rec', 'rec_yds']},
    'name': 'Pro Football Reference'
}

def get_url() -> tuple:
    urls = {
        '1': PFR,
    }

    print('Website Choices:')

    for key in urls:
        name = urls[key]['name']
        print(f'{key}. {name}')

    choice = input('Choose a url by its number: ')

    return (urls[choice]['base'], urls[choice]['pos']['QB'])

def main():
    url = get_url()
    print(url)

main()