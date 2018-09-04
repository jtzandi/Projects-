import pandas as pd
import sys
import geopandas as gpd
import csv
import shapely

#full list of intersections (intersect.csv)
intersections = open(sys.argv[1]) #read in NYC intersections shapefile
reader = csv.reader(intersections, delimiter=',')

# infile csv as dataframe (clean fatalities/injuries csv)
df = pd.read_csv(sys.argv[2], sep=',')

#index on NODEID
df.set_index('NODEID', inplace=True)
#outfile csv
outfile = open(sys.argv[3],'w') #read in output csv file
writer = csv.writer(outfile)

#make row dicts for easier indexing
header = next(reader, None) #read in header row
enum_header = enumerate(header)
header_dict = {}
for num,index in enum_header:
    header_dict[index] = num

#write header
out_header = ('NODEID','Lon','Lat','MN','YR','Fatalities_COUNT','PedFatalit_COUNT','BikeFatali_COUNT','MVOFatalit_COUNT','Fatalities','PedFatalit','BikeFatali', 'MVOFatalit')
writer.writerow(out_header) #write header row

#iterate every intersection
for row in reader:
    node_id = int(row[header_dict['NODEID']])
    lon = row[header_dict['Lon']]
    lat = row[header_dict['Lat']]

    #if the intersection node = accident node, true. else false.
    if node_id in df.index:
        try:
            mon = int(df.loc[node_id]['MN'])
            yr = int(df.loc[node_id]['YR'])
            fat = int(df.loc[node_id]['Fatalities'])
            ped = int(df.loc[node_id]['PedFatalit'])
            bike = int(df.loc[node_id]['BikeFatali'])
            mvo = int(df.loc[node_id]['MVOFatalit'])
            fat_count = int(df.loc[node_id]['Fatalities_COUNT'])
            ped_count = int(df.loc[node_id]['PedFatalit_COUNT'])
            bike_count = int(df.loc[node_id]['BikeFatali_COUNT'])
            mvo_count = int(df.loc[node_id]['MVOFatalit_COUNT'])
            writer.writerow((node_id, lon, lat, mon, yr, fat_count,ped_count,bike_count,mvo_count,fat, ped, bike, mvo))
        except:
            for index,row in df.loc[node_id].iterrows():
                mon = int(row['MN'])
                yr = int(row['YR'])
                fat = int(row['Fatalities'])
                ped = int(row['PedFatalit'])
                bike = int(row['BikeFatali'])
                mvo = int(row['MVOFatalit'])
                fat_count = int(row['Fatalities_COUNT'])
                ped_count = int(row['PedFatalit_COUNT'])
                bike_count = int(row['BikeFatali_COUNT'])
                mvo_count = int(row['MVOFatalit_COUNT'])
                writer.writerow((node_id, lon, lat, mon, yr, fat_count,ped_count,bike_count,mvo_count,fat, ped, bike, mvo))

    else:
        writer.writerow((node_id, lon, lat,0,2016,0,0,0,0,0,0,0,0))

intersections.close()
outfile.close()
