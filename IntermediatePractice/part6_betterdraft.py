from bs4 import BeautifulSoup as BS
import requests
import pandas as pd

def remove_trailing_crap(ply_str):
    ply_lst = ply_str.split()
    team_names = ["ARI", "ATL", "BAL", "BUF", "CAR", "CIN", "CHI", "CLE", "DAL", "DEN", "DET", "GB", 
    "HOU", "IND", "JAX", "KC", "LAC", "LAR", "LV", "MIA", "MIN", "NE", "NO", "NYG", "NYJ", "PHI", 
    "PIT", "SEA", "SF", "TB", "TEN", "WAS"]

    index = 0
    for x in ply_lst:
        if x in team_names:
            break
        else:
            index += 1
    
    return ' '.join(ply_lst[:index])

def make_adp_df(BASE_URL = "https://www.fantasypros.com/nfl/adp/ppr-overall.php") -> pd.DataFrame():
    res = requests.get(BASE_URL)
    if res.ok:
        soup = BS(res.content, 'html.parser')
        table = soup.find('table', {'id': 'data'})
        df = pd.read_html(str(table))[0]
        #print('Output after reading the html:\n\n', df.head(), '\n') # so you can see the output at this point
        df = df[['Player Team (Bye)', 'POS', 'AVG']]
        #print('Output after filtering:\n\n', df.head(), '\n')
        #df['PLAYER'] = df['Player Team (Bye)'].apply(lambda x: ' '.join(x.split()[:-2])) # removing the team and position

        df['PLAYER'] = df['Player Team (Bye)'].apply(lambda x: remove_trailing_crap(x))

        df['POS'] = df['POS'].apply(lambda x: x[:2]) # removing the position rank
        
        df = df[['PLAYER', 'POS', 'AVG']].sort_values(by='AVG')
        
        #print('Final output: \n\n', df.head())
        
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


def make_projection_df(BASE_URL = 'https://www.fantasypros.com/nfl/projections/{position}.php?week=draft') -> pd.DataFrame():
    final_df = pd.DataFrame()

    for pos in ['rb', 'qb', 'te', 'wr']:
        res = requests.get(BASE_URL.format(position=pos))

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

adp_df = make_adp_df()
rp = make_replacement_players(adp_df)

df = make_projection_df()
rv = make_replacement_values(df, rp)

df['VOR'] = df.apply(lambda row: row['FPTS'] - rv.get(row['POS']), axis=1)

df = df.sort_values(by='VOR', ascending=False)
df['VALUERANK'] = df['VOR'].rank(ascending=False)

adp_df['ADPRANK'] = adp_df['AVG'].rank(method='first')

df = df.merge(adp_df, how='left', on=['PLAYER', 'POS'])

df['SLEEPERSCORE'] = df['ADPRANK'] - df['VALUERANK']
print(df.loc[df['AVG'] < 192].sort_values(by='SLEEPERSCORE', ascending=False).head(15))

#print(adp_df.head(30))
#print(df.head(25))