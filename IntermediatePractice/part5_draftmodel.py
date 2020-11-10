import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

BASE_URL = "https://www.fantasypros.com/nfl/adp/ppr-overall.php"

def make_adp_df() -> pd.DataFrame():
    res = requests.get(BASE_URL)
    if res.ok:
        soup = BS(res.content, 'html.parser')
        table = soup.find('table', {'id': 'data'})
        df = pd.read_html(str(table))[0]
        print('Output after reading the html:\n\n', df.head(), '\n') # so you can see the output at this point
        df = df[['Player Team (Bye)', 'POS', 'AVG']]
        print('Output after filtering:\n\n', df.head(), '\n')
        df['PLAYER'] = df['Player Team (Bye)'].apply(lambda x: ' '.join(x.split()[:-2])) # removing the team and position
        df['POS'] = df['POS'].apply(lambda x: x[:2]) # removing the position rank
        
        df = df[['PLAYER', 'POS', 'AVG']].sort_values(by='AVG')
        
        print('Final output: \n\n', df.head())
        
        return df
        
    else:
        print('oops, something didn\'t work right', res.status_code)

def make_replacement_values(df, rp) -> dict:
    replacement_values = {'RB': 0, 'WR': 0, 'TE': 0, 'QB': 0}

    for pos, ply in rp.items():
        if pos in ['RB', 'WR', 'TE', 'QB']:
            replacement_values[pos] = df.loc[df['PLAYER'] == ply].values[0, -1]
    
    return replacement_values


def make_replacement_players(df) -> dict:
    replacement_players = { 'RB': '', 'WR': '', 'TE': '', 'QB': '' }

    for _, row in df[:100].iterrows():
        position = row['POS']
        player = row['PLAYER']
        replacement_players[position] = player
    
    return replacement_players

NEW_URL = 'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft'

def make_projection_df() -> pd.DataFrame():
    final_df = pd.DataFrame()

    for pos in ['rb', 'qb', 'te', 'wr']:
        res = requests.get(NEW_URL.format(position=pos))

        if res.ok:
            soup = BS(res.content, 'html.parser')
            table = soup.find('table', {'id': 'data'})
            df = pd.read_html(str(table))[0]

            df.columns = df.columns.droplevel(level=0)
            df['PLAYER'] = df['Player'].apply(lambda x: ' '.join(x.split()[:-1]))

            if 'REC' in df.columns:
                df['FPTS'] = df['FPTS'] + df['REC']

            df['POS'] = pos.upper()

            df = df[['PLAYER', 'POS', 'FPTS']]
            final_df = pd.concat([final_df, df])
        else:
            print('something broke', res.status_code)
            return

    final_df = final_df.sort_values(by='FPTS', ascending=False)

    return final_df

df = make_adp_df()
rp = make_replacement_players(df)

df = make_projection_df()

rv = make_replacement_values(df, rp)

df['VOR'] = df.apply(    lambda row: row['FPTS'] - rv.get(row['POS']), axis=1)

df = df.sort_values(by='VOR', ascending=False)
df['VALUERANK'] = df['VOR'].rank(ascending=False)

print(df.head(100))