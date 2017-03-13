import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def load_clean(fpath, team1='W', team2='L', outcome=1):
    reg_df = pd.read_csv(fpath)
    cols = reg_df.columns.tolist()
    wcols = []
    lcols = []
    for col in cols:
        if col[0] == team1:
            wcols.append('{}1'.format(col[1:]))
        elif col[0] == team2:
            wcols.append('{}2'.format(col[1:]))
        else:
            wcols.append(col)
    reg1 = pd.DataFrame()
    reg1[wcols] = reg_df[cols].copy()
    reg1['outcome'] = outcome
    return reg1

cols_to_drop = ['team2', 'Daynum', 'outcome']

def get_season_stats(fpath, drop=cols_to_drop):
    wdf = load_clean(fpath)
    ldf = load_clean(fpath, team1='L', team2='W', outcome=0)
    reg_df = pd.concat([wdf,ldf])
    season = reg_df.groupby(['Season', 'team1'], as_index=False).mean()
    season['winpct'] = season['outcome']
    for col in drop:
        season.pop(col)
    return reg_df[['Season', 'team1', 'Daynum', 'outcome']], season

# def merge_game_season(games, season):


if __name__ == '__main__':
    fpath = '../data/RegularSeasonDetailedResults.csv'
    game, season = get_season_stats(fpath)
    df = game.merge(season, on=['Season', 'team1'], how='inner')
