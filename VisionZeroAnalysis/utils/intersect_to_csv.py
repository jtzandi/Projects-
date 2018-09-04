import pandas as pd
import sys
import geopandas as gpd
import csv
import shapely

intersections = gpd.read_file(sys.argv[1]) #read in NYC intersections shapefile
intersections = intersections.to_crs(({'init': 'epsg:4326'})) #transform to WSG84 4326 format

outfile = open(sys.argv[2],'w') #read in output csv file
writer = csv.writer(outfile)

header = ('NODEID','Lon','Lat')
writer.writerow(header) #write header row

for index,row in intersections.iterrows():
    node_id = row['NODEID']
    coords = list(row['geometry'].coords)
    lon = coords[0][0]
    lat = coords[0][1]
    writer.writerow((node_id, lon, lat))

outfile.close()
