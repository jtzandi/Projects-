import pandas as pd
import sys

#load temp CSV into pandas DF
df = pd.read_csv(sys.argv[1], sep=',')

#filter for only 2016 values
#NOTE: Change 2016 to string for fatality_monthly_temp.csv only.
df1 = df[df['YR'] == 2016]

#keep only desired columns
cols_to_keep = ['FID', 'MN', 'YR', 'NODEID','Lon','Lat','Injuries','PedInjurie','BikeInjuri','MVOInjurie']
df1 = df1[cols_to_keep]

df1.rename(columns={'Injuries': 'Injuries_COUNT', 'PedInjurie': 'PedInjurie_COUNT', 'BikeInjuri': 'BikeInjuri_COUNT','MVOInjurie':'MVOInjurie_COUNT' }, inplace=True)

#change to fatality/injury from continuous to categorical
df1['Injuries'] = df1['Injuries_COUNT'].apply(lambda x: 1 if x >= 1 else 0)
df1['PedInjurie'] = df1['PedInjurie_COUNT'].apply(lambda x: 1 if x >= 1 else 0)
df1['BikeInjuri'] = df1['BikeInjuri_COUNT'].apply(lambda x: 1 if x >= 1 else 0)
df1['MVOInjurie'] = df1['MVOInjurie_COUNT'].apply(lambda x: 1 if x >= 1 else 0)

#write out to CSV
df1.to_csv(sys.argv[2], index=False)
