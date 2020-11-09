import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

def covariance(x, y):
    n = len(x)
    return sum((x - np.mean(x)) * (y - np.mean(y))) * 1/(n-1)

def correlation(x, y):
    return covariance(x, y)/(np.std(x) * np.std(y))

csv_path = '2019.csv'

df = pd.read_csv(csv_path)

df = df.loc[df['Pos'] == 'RB', ['Player', 'Tgt', 'RushingAtt', 'FantasyPoints']]
df['Usage'] = df['Tgt'] + df['RushingAtt']

df['UsageRank'] = df['Usage'].rank(ascending=False)
df['FantasyPointsRank'] = df['FantasyPoints'].rank(ascending=False)

df.sort_values(by='UsageRank').head()

X = df['Usage'].values
Y = df['FantasyPoints'].values
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)