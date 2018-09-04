import csv, shapely, sys, os
import geopandas as gpd
from pathlib import Path
#import matplotlib.pyplot as plt

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
                if shape.almost_equals(point,decimal=2):
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
                pass
        except: #its a multishape and we must iterate
            pass

    if len(point_list) > 0:
        row.append(1)
        writer.writerow(row)
    else:
        row.append(0)
        writer.writerow(row)

for file in os.listdir('../initiatives'):
    if not file.startswith('.'):
        infile = open('in.csv')
        reader = csv.reader(infile, delimiter=',')
        path = '../initiatives/' + file
        input_file = gpd.read_file(path)
        outfile = open('out.csv','w')
        writer = csv.writer(outfile)

        #add a column
        header = next(reader) #read in header row
        column_name = file.split('.')[0] #extract desired column name specificed in command line sys.argv[2]

        try:
            header.append(column_name) #add column label
            writer.writerow(header)

        except:
            header.append(file) #add column label
            writer.writerow(header)

        #make row dictionary (e.g. header_dict['BikeZone'] == 3)
        enum_header = enumerate(header)
        header_dict = {}
        for num,index in enum_header:
            header_dict[index] = num

        for row in reader:
            point = extract_point(row) #creates shapely Point object
            geo = input_file['geometry']
            attribute_check(row,point,geo)

    infile.close()
    outfile.close()

    os.remove('in.csv')
    os.rename('out.csv','in.csv')
    Path('out.csv').touch()
