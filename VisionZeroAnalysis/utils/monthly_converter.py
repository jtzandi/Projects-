from pyproj import Proj, transform
import csv

infile = open('data/fatality_monthly.csv','r')
reader = csv.reader(infile,delimiter=',')
outfile = open('data/clean/fatality_monthly_clean.csv','w')
writer = csv.writer(outfile)

header = next(reader,None) #skip first line
print(header)
writer.writerow(('FID', 'Join_Count', 'TARGET_FID','Fatalities','PedFatalit','BikeFatali','MVOFatalit','MN','YR','NODEID','Lon','Lat','STREET1','STREET2'))

input = Proj(init='epsg:2263', preserve_units=True)
output = Proj(init='epsg:4326')

for row in reader:
    x1 = row[10]
    y1 = row[11]
    lon,lat = transform(input,output,x1,y1)
    writer.writerow((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],lon,lat,row[12],row[13]))

infile.close()
outfile.close()
