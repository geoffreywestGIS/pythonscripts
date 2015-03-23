import xml.etree.ElementTree as ET
import urllib
import os
import arcpy


u = urllib.urlopen('https://api.octranspo1.com/v1.1/GetNextTripsForStop', 'appID=7a51d100&apiKey=5c5a8438efc643286006d82071852789&routeNo=95&stopNo=3008')
data = u.read()

f = open('route3008.xml', 'wb')
f.write(data)
f.close()

doc = ET.parse('route3008.xml')

for bus in doc.findall('.//{http://tempuri.org/}Trip'):
    lat = bus.findtext('{http://tempuri.org/}Latitude')
    lon = bus.findtext('{http://tempuri.org/}Longitude')
    print lat, lon




#f = open("C:\Users\GIS\Desktop\pyCharm.txt","w")
#print >> f, 'Lat/Lng:', [lat, lon]  # or f.write('...\n')
#f.close()


#Write XY to CSV
import csv
arcpy.env.workspace = 'C:\pyCharm\pyCharm.gdb'
arcpy.env.overwriteOutput = 'True'

with open('C:\Users\GIS\Desktop\pycharm.csv', 'w') as file:
    fieldnames = ['X', 'Y']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'X': lon, 'Y': lat})

outputname = 'EventTest2'
table = 'C:\Users\GIS\Desktop\pycharm.csv'
outputGDB = 'C:\pyCharm\pyCharm.gdb'
arcpy.TableToTable_conversion(table,outputGDB, outputname)

#Set Output of EventXY to Feature Class in Geodatabase
arcpy.MakeXYEventLayer_management("EventTest2", "X", "Y")
arcpy.FeatureClassToFeatureClass_conversion("EventTest2_Layer", "C:\pyCharm\pyCharm.gdb", "MakeEventLayer2")
