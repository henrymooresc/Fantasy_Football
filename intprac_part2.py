import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

pd.options.mode.chained_assignment = None

# Imports CSV
df = pd.read_csv('2019.csv')

# Drop unneccessary columns
df.drop([
    'Rk', '2PM', '2PP', 'FantPt', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 
    'Fmb', 'GS', 'Age', 'Tgt', 'Y/A', 'Att', 'Att.1', 'Cmp', 'Y/R'
    ], axis=1, inplace=True)

# Fix name formatting
df['Player'] = df['Player'].apply(lambda x: x.split('*')[0]).apply(lambda x: x.split('\\')[0])

# Rename columns
df.rename({
    'TD': 'PassingTD',
    'TD.1': 'RushingTD',
    'TD.2': 'ReceivingTD',
    'TD.3': 'TotalTD',
    'Yds': 'PassingYDs',
    'Yds.1': 'RushingYDs',
    'Yds.2': 'ReceivingYDs',
    'Att': 'PassingAtt',
    'Att.1': 'RushingAtt'
}, axis=1, inplace=True)

# Calc 0.5 PPR points
df['FantasyPoints'] = (
    df['PassingYDs']*0.04 * df['PassingTD']*4 - df['Int']*2 + df['RushingYDs']*0.1 + 
    df['RushingTD']*6 + df['Rec']*1 + df['ReceivingYDs']*0.1 + df['ReceivingTD']*6 - df['FL']*2
    )

df['FantasyPoints/GM'] = df['FantasyPoints'] / df['G']

# Limited DataFrame?
df = df[df['Tm'] != '2TM']
df = df[df['Tm'] != '3TM']

rb_df = df[df['FantPos'] == 'RB']
rb_df['Rec/G'] = rb_df['Rec']/rb_df['G']
rb_df = rb_df[rb_df['Rec'] > 5]

df = df[['Tm', 'FantPos', 'FantasyPoints', 'FantasyPoints/GM']]
rb_df = df[['Tm', 'FantPos', 'FantasyPoints', 'FantasyPoints/GM']]

rb_df = rb_df[rb_df['Tm'] != '2TM']
rb_df = rb_df[rb_df['Tm'] != '3TM']

#seperate dataframes based off position
qb_df = df[df['FantPos'] == 'QB']
wr_df = df[df['FantPos'] == 'WR']
te_df = df[df['FantPos'] == 'TE']

rb_df.head()

def get_top_players(df, n):
    return df.groupby('Tm').apply(lambda x: x.nlargest(n, ['FantasyPoints']).min()).reset_index(drop=True)

qb_df = get_top_players(qb_df, 1)
te_df = get_top_players(te_df, 1)
rb1_df = get_top_players(rb_df, 1)
rb2_df = get_top_players(rb_df, 2)
wr1_df = get_top_players(wr_df, 1)
wr2_df = get_top_players(wr_df, 2)
wr3_df = get_top_players(wr_df, 3)

new_names = {
    'QB1': qb_df,
    'TE1': te_df,
    'RB1': rb1_df,
    'RB2': rb2_df,
    'WR1': wr1_df,
    'WR2': wr2_df,
    'WR3': wr3_df
}

for name, new_df in new_names.items():
    new_df.rename({'FantasyPoints/GM': name}, axis=1, inplace=True)
    new_df.drop(['FantPos', 'FantasyPoints'], axis=1, inplace=True)
    new_df.set_index('Tm', inplace=True)
    
df = pd.concat([qb_df, te_df, rb1_df, rb2_df, wr1_df, wr2_df, wr3_df], axis=1)

df.head()

corrMatrix = df.corr()

cmap = sns.diverging_palette(0, 250, as_cmap=True)

#This is for the Part 3 of the Python for Fantasy Football Analysis

fig, ax = plt.subplots()
fig.set_size_inches(15, 10)

mask = np.zeros_like(corrMatrix, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

vizCorrMatrix = sns.heatmap(corrMatrix, mask=mask,cmap=cmap, center=0)

plt.show()