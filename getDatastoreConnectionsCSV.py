# Connect to  ArcGIS Enterprise Portal and import libraries 
from arcgis.gis import GIS
import csv

# Sign in to the appropriate portal using ArcGIS Pro prior to runing tool
gis = GIS("pro")

servers = gis.admin.servers.list()
server1 = servers[0]
dstores = server1.datastores.list()

with open("C:\Temp\dstoresT1.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Dstore Name", "Connection String"])
    
    for dstore in dstores:
        try:
            name = getattr(dstore.properties, "path", "unknown")
            connection_string = getattr(dstore.properties.info, "connectionString", "unknown")
            writer.writerow([name, connection_string])
        except:
            print('False')
