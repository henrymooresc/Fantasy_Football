import pandas as pd
from sklearn.utils import resample
from matplotlib import pyplot as plt
import numpy as np
import itertools
import seaborn as sns; sns.set_style('whitegrid')

# manual projections
df = pd.DataFrame({
    'Player': ['Juju Smith-Schuster', 'Devante Parker', 'Tyler Boyd'],
    'Sleeper': [16.20, 13.92, 14.23],
    'FanDuel': [15.84, 12.20, 11.92],
    'ESPN': [14.60, 12.50, 11.70],
    'FantasyPros': [15.60, 11.70, 12.30],
    'fftoday': [14.60, 13.10, 7.60],
    'ffcalculator': [16.20, 14.0, 14.50],
    'walterfootball': [18.0, 10.0, 10.0]
})

# grabbing each weekly points as an array
juju = df.iloc[0, 1:].values
parker = df.iloc[1, 1:].values
boyd = df.iloc[2, 1:].values

def calculate_bootstrap_df(*proj_points_arrays, player_names=None, n_iterations=10000) -> pd.DataFrame:
    df_data = {}

    for i, arr in enumerate(proj_points_arrays):

        proj_points_means = []

        for n in range(n_iterations):
            # find bootstrap resample array
            boot = resample(arr, n_samples=len(arr))
            # append the mean of the bootstrap array to a list of means
            proj_points_means.append(np.mean(boot))

        # if player names are provided, set the names as the column, otherwise give defaults
        if player_names:
            df_data[player_names[i]] = proj_points_means
        else:
            df_data[f'player_{i+1}'] = proj_points_means

    return pd.DataFrame(df_data)

def plot_kde(*args, figsize=(10, 8), **kwargs):
    # Plot each player's bootstrapped means as a kernel density estimation

    df = calculate_bootstrap_df(*args, **kwargs) # get bootstrap df
    df.plot.kde() # plot as kernel density estimation

    fig, ax = plt.gcf(), plt.gca() # get current figure, axis from above
    fig.set_size_inches(figsize)
    colors = itertools.cycle(['blue', 'orange', 'green', 'orange'])

    for i, (arr, color) in enumerate(zip(args, colors)):
        l = ax.lines[i]
        x = l.get_xydata()[:,0]
        y = l.get_xydata()[:,1]

        ax.fill_between(x, y, color=color, alpha=0.2) # fill the area underneath the KDE plots with their associated color

        x_loc = x[np.where(y == y.max())[0]] # find the x-location of the max of each KDE

        ax.vlines(x=x_loc, ymax=y.max(), ymin=0, linestyles='dashed', alpha=0.5, color=color) # plot a vertical line leading up to the max of the KDE

    plt.show()

def calculate_ceiling_floor(*arrays, player_names=None, stdout=False):

    data = {}

    for i, arr in enumerate(arrays):
        boot = calculate_bootstrap_df(arr).values

        mean = boot.mean() # find the mean of the means

        ceiling = np.percentile(boot, 95) # find the upper bound of the confidence interval
        floor = np.percentile(boot, 5) # find the lower bound of the confidence interval

        player_data = {
            'mean': mean,
            'ceiling': ceiling,
            'floor': floor
        }

        if player_names:
            data[player_names[i]] = player_data
        else:
            data[f'player_{i+1}'] = player_data

    if stdout:
        for player, player_data in data.items():
            print(player, 'has a mean projected output of', round(player_data['mean'], 2), \
                'a ceiling of', round(player_data['ceiling'], 2), 'and a floor of', round(player_data['floor'], 2))
            print('\n')

    return data

plot_kde(juju, parker, boyd, player_names=['Juju', 'Parker', 'Boyd'])

print(calculate_bootstrap_df(juju, parker, boyd, player_names=['Juju', 'Parker', 'Boyd']).head(5))

data = calculate_ceiling_floor(juju, parker, boyd, player_names=['Juju Smith-Schuster', 'Devante Parker', 'Tyler Boyd'], stdout=True)