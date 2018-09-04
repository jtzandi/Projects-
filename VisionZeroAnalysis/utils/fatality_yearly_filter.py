import pandas as pd
import sys

#load 'temp' CSV into pandas DF
df = pd.read_csv(sys.argv[1], sep=',')

#filter for only 2016 values
df1 = df[df['YR'] == 2016]

#keep only certain columns
cols_to_keep = ['FID', 'YR', 'NODEID','Lon','Lat', 'Fatalities', 'PedFatalit','BikeFatali','MVOFatalit']
df1 = df1[cols_to_keep]

#change to fatality/injury from continuous to categorical
df1.rename(columns={'Fatalities': 'Fatalities_COUNT', 'PedFatalit': 'PedFatalit_COUNT', 'BikeFatali': 'BikeFatali_COUNT','MVOFatalit':'MVOFatalit_COUNT' }, inplace=True)

df1['Fatalities'] = df1['Fatalities_COUNT'].apply(lambda x: 1 if x >= 1 else 0)
df1['PedFatalit'] = df1['PedFatalit_COUNT'].apply(lambda x: 1 if x >= 1 else 0)
df1['BikeFatali'] = df1['BikeFatali_COUNT'].apply(lambda x: 1 if x >= 1 else 0)
df1['MVOFatalit'] = df1['MVOFatalit_COUNT'].apply(lambda x: 1 if x >= 1 else 0)

#write out to csv (clean.csv)
df1.to_csv(sys.argv[2], index=False)
