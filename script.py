import pandas as pd
import numpy as np

# Set settings for dataframe
pd.set_option('display.max_rows', 1000)
pd.options.display.max_colwidth = 150
pd.set_option('display.max_columns', None)

# Let's bring it in
df = pd.read_csv('/Users/sm029588/OneDrive - Cerner Corporation/PycharmProjects/Billboard-Hot-100/Hot 100.csv', parse_dates=['chart_date'])

# Need to test new code on a subset?
# df = df.loc[df['song_id'] == 'All I Want For Christmas Is YouMariah Carey']

# Good to make sure everything is sorted properly
df.sort_values(['song_id', 'chart_date'], ascending=[True, True], inplace=True)
df.reset_index(drop=True, inplace=True)

# When was the first time a song landed on the chart?
df['chart_debut'] = df.groupby('song_id')["chart_date"].transform('min')

# How many total weeks has it been since the debut?
df['time_on_chart'] = df.groupby('song_id').cumcount() + 1

# For each song, let's find out how many consecutive weeks it's been on the chart
df['days_since_last'] = df.groupby(['song_id'])['chart_date'].diff()
df.loc[df['days_since_last'] == '7 days', 'is_consecutive'] = 1
df.loc[df['days_since_last'] != '7 days', 'is_consecutive'] = 0
df.loc[df['is_consecutive'] == 0, 'reset'] = 1
df.loc[df['is_consecutive'] == 1, 'reset'] = 0
df['cumsum'] = df['reset'].cumsum()
df['consecutive_weeks'] = df.groupby(['song_id','cumsum'])['is_consecutive'].cumsum()

# How many times has a song reappeared on the chart
df['instance'] = df.groupby('song_id')['reset'].cumsum()

# What was the song's previous rank
df['previous_rank'] = df.groupby(['song_id'])['chart_position'].shift(1)
df.loc[df['days_since_last'] == '7 days', 'previous_week'] = df['previous_rank']
df.loc[df['days_since_last'] != '7 days', 'previous_week'] = 0

# What's the highest & lowest position a song has been
df['peak_position'] = df.groupby(['song_id'])['chart_position'].cummin()
df['worst_position'] = df.groupby(['song_id'])['chart_position'].cummax()

# Null out the zeros
df['consecutive_weeks'] = df['consecutive_weeks'].replace(0, np.nan)
df['previous_week'] = df['previous_week'].replace(0, np.nan)

# Output
df.to_csv('/Users/sm029588/OneDrive - Cerner Corporation/PycharmProjects/Billboard-Hot-100/Hot 100.csv', index=False, columns=['chart_position', 'chart_date', 'song', 'performer', 'song_id','instance', 'time_on_chart', 'consecutive_weeks', 'previous_week', 'peak_position', 'worst_position', 'chart_debut', 'chart_url'])
# print(df)