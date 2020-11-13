import pandas as pd # Python's data munging library
from bs4 import BeautifulSoup as BS # Python's web scraping library
import requests # Python's library for making HTTP requests
from matplotlib import pyplot as plt # for visualizing the data
import seaborn as sns # for styling the visualizations
import numpy as np # for doing some maths

ALL_URLS = {
    'Pro Football Reference': {
        'Weekly Player': {
            'base': 'https://stathead.com/football/pgl_finder.cgi?request=1&match=game&year_min={year}&year_max={year}&season_start=1&season_end=-1&age_min=0&age_max=99&game_type=A&league_id=&team_id=&opp_id=&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&game_day_of_week=&game_location=&game_result=&handedness=&is_active=&is_hof=&c1stat={opt1}&c1comp=gt&c1val=1&c2stat=&c2comp=gt&c2val=&c3stat=&c3comp=gt&c3val=&c4stat=&c4comp=gt&c4val=&order_by={opt2}&from_link=1',
            'pos': {'QB': ['pass_att', 'pass_rating'], 'RB': ['rush_att', 'rush_yds'], 'WR': ['rec', 'rec_yds']}
        },
        'Team Defense': {
            'base': 'https://stathead.com/football/tgl_finder.cgi?request=1&match=game&order_by_asc=1&order_by=points_opp&year_min={year}&year_max={year}&game_type=R&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&temperature_gtlt=lt'
        },
        'Kicking': {
            'base': 'https://stathead.com/football/pgl_finder.cgi?request=1&match=game&order_by_asc=0&order_by=fgm&year_min={year}&year_max={year}&game_type=R&positions[]=k&age_min=0&age_max=99&game_num_min=0&game_num_max=99&week_num_min={week}&week_num_max={week}&season_start=1&season_end=-1'
        }
    }
}

def get_choices() -> list:
    # runs through possible choices for urls, returns the formatted string
    print('Website Choices:')
    web_choice = make_choices(ALL_URLS)

    print('Stat Type Choices:')
    stat_choice = make_choices(ALL_URLS[web_choice])

    url_string = ALL_URLS[web_choice][stat_choice]['base']

    game_choice = input('Enter a season year and week number (i.e. 2019 3): ')
    date = game_choice.split(' ')

    # two different format types currently and .format doesn't like not assigning everything at once
    if stat_choice == 'Weekly Player':
        print('Position Choices:')
        pos_choice = make_choices(ALL_URLS[web_choice][stat_choice]['pos'])
        url_string = url_string.format(year=int(date[0]), week=int(date[1]), opt1=ALL_URLS[web_choice][stat_choice]['pos'][pos_choice][0], opt2=ALL_URLS[web_choice][stat_choice]['pos'][pos_choice][1])
    else:
        url_string = url_string.format(year=int(date[0]), week=int(date[1]))

    return [web_choice, stat_choice, date, url_string]


def make_choices(dict_of_choices: dict):
    # got tired of rewriting a dumb loop since I'm too stubborn to change my dict structure
    # Loops through the passed dictonary "ordering" it to allow easy user numerial input
    i = 1
    c = []

    for k in dict_of_choices:
        print(f'{i}. {k}')
        c.append(k)
        i += 1

    # returns the choice if valid, if not it recursively tries again
    try:
        return c[int(input(f'Choose by entering a number: ')) - 1]
    except IndexError:
        print('Bad input, try again')
        return make_choices(dict_of_choices)

def main():
    choices_list = get_choices()

    if choices_list[0] == 'Pro Football Reference':
        print(f'Pulling {choices_list[1]} data from {choices_list[0]} for week {choices_list[2][1]} of the {choices_list[2][0]} season')

main()