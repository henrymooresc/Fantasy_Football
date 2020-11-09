import pandas as pd

csv_path = '2019.csv'

df = pd.read_csv(csv_path)

df = df.loc[df['Pos'] == 'RB', ['Player', 'Tgt', 'RushingAtt', 'FantasyPoints']]
df['Usage'] = df['Tgt'] + df['RushingAtt']

df['UsageRank'] = df['Usage'].rank(ascending=False)
df['FantasyPointsRank'] = df['FantasyPoints'].rank(ascending=False)

print(df.sort_values(by='UsageRank').head(15))