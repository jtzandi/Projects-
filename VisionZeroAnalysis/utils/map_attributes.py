import csv, shapely, sys, os
import geopandas as gpd
from pathlib import Path

#read in input CSV file
# infile = open('data/clean/fatality_yearly_clean.csv')
infile = open(sys.argv[1])
reader = csv.reader(infile, delimiter=',')

outfile = open(sys.argv[3],'w')
writer = csv.writer(outfile)

#read in data (using file path as sys.argv[2])
try:
    input_file = gpd.read_file(sys.argv[2])
    geo = input_file.geometry

except:
    print('Input file not found, please try again')
    sys.exit()

#add a column
header = next(reader, None) #read in header row
column_name = sys.argv[2].split('/')[-1].split('.')[0] #extract desired column name specificed in command line sys.argv[2]

header.append(column_name) #add column label
writer.writerow(header)

#make row dictionary (e.g. header_dict['BikeZone'] == 3)
enum_header = enumerate(header)
header_dict = {}
for num,index in enum_header:
    header_dict[index] = num

#make a point from CSV
def extract_point(row):
    lon = float(row[header_dict['Lon']])
    lat = float(row[header_dict['Lat']])
    point = shapely.geometry.Point(lon, lat)
    return point

def attribute_check(row, point, geo):
    point_list = []
    for key,shape in geo.iteritems():
        try: #its an geometric object
            type = shape.geom_type
            if type == 'Polygon':
                if shape.contains(point):
                    point_list.append(point)
                    break
                else:
                    pass
            elif type == 'LineString':
                if shape.distance(point) < 1e-8:
                    point_list.append(point)
                    break
                else:
                    pass
            elif type == 'Point':
                if shape.almost_equals(point,decimal=4):
                    point_list.append(point)
                    break
                else:
                    pass
            elif type == 'MultiLineString':
                lines = list(shape.geoms)
                for line in lines:
                    if line.distance(point) < 1e-8:
                        point_list.append(point)
                        break
                    else:
                        pass
            else:
                print(row)
        except: #its a multishape and we must iterate
            print(type, row)

    if len(point_list) > 0:
        row.append(1)
        writer.writerow(row)
    else:
        row.append(0)
        writer.writerow(row)

for row in reader:
    point = extract_point(row) #creates shapely Point object
    attribute_check(row, point, geo) #checks to see if point in polygon and writes 1 to column if True, 0 if false

infile.close()
outfile.close()
