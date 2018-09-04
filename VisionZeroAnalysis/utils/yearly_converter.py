from pyproj import Proj, transform
import csv

infile = open('data/fatality_yearly.csv','r')
reader = csv.reader(infile,delimiter=',')
outfile = open('data/clean/fatality_yearly_clean.csv','w')
writer = csv.writer(outfile)

header = next(reader,None) #skip first line
print(header)
writer.writerow(('FID', 'Join_Count', 'TARGET_FID','Fatalities','PedFatalit','BikeFatali','MVOFatalit','YR','NODEID','Lon','Lat','STREET1','STREET2'))

input = Proj(init='epsg:2263', preserve_units=True)
output = Proj(init='epsg:4326')

for row in reader:
    x1 = row[9]
    y1 = row[10]
    lon,lat = transform(input,output,x1,y1)
    writer.writerow((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],lon,lat,row[11],row[12]))

infile.close()
outfile.close()
