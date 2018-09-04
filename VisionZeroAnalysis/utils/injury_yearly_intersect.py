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
out_header = ('NODEID','Lon','Lat','YR','Injuries_COUNT','PedInjurie_COUNT','BikeInjuri_COUNT','MVOInjurie_COUNT','Injuries','PedInjurie','BikeInjuri', 'MVOInjurie')
writer.writerow(out_header) #write header row

#iterate every intersection
for row in reader:
    node_id = int(row[header_dict['NODEID']])
    lon = row[header_dict['Lon']]
    lat = row[header_dict['Lat']]

    #if the intersection node = accident node, true. else false.
    if node_id in df.index:
        try:
            yr = int(df.loc[node_id]['YR'])
            inj = int(df.loc[node_id]['Injuries'])
            ped = int(df.loc[node_id]['PedInjurie'])
            bike = int(df.loc[node_id]['BikeInjuri'])
            mvo = int(df.loc[node_id]['MVOInjurie'])
            inj_count = int(df.loc[node_id]['Injuries_COUNT'])
            ped_count = int(df.loc[node_id]['PedInjurie_COUNT'])
            bike_count = int(df.loc[node_id]['BikeInjuri_COUNT'])
            mvo_count = int(df.loc[node_id]['MVOInjurie_COUNT'])
            writer.writerow((node_id, lon, lat, yr, inj_count,ped_count,bike_count,mvo_count,inj, ped, bike, mvo))
            #print(node_id, lon, lat, mon, yr, inj_count,ped_count,bike_count,mvo_count,inj, ped, bike, mvo)
        except:
            if isinstance(df.loc[node_id], pd.DataFrame):
                for index,row in df.loc[node_id].iterrows():
                    yr = int(row['YR'])
                    inj = int(row['Injuries'])
                    ped = int(row['PedInjurie'])
                    bike = int(row['BikeInjuri'])
                    mvo = int(row['MVOInjurie'])
                    inj_count = int(row['Injuries_COUNT'])
                    ped_count = int(row['PedInjurie_COUNT'])
                    bike_count = int(row['BikeInjuri_COUNT'])
                    mvo_count = int(row['MVOInjurie_COUNT'])
                    writer.writerow((node_id, lon, lat, yr, inj_count,ped_count,bike_count,mvo_count,inj, ped, bike, mvo))
            else:
                print('ERROR')
    else:
        writer.writerow((node_id, lon, lat,2016,0,0,0,0,0,0,0,0))

intersections.close()
outfile.close()
