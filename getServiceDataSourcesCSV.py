# Connect to  ArcGIS Enterprise Portal and import libraries 
from arcgis.gis import GIS
import csv

# Sign in to the appropriate portal using ArcGIS Pro prior to runing tool
gis = GIS("pro")

servers = gis.admin.servers.list()
server1 = servers[0]
folders = [""] + server1.services.folders # this will iterate through the entire ArcGIS REST Services Directory

# replace with desired output directory for the .csv
with open(r'C:\Temp\allServices.csv', mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Service Name", "Data Source"])
    
    for folder in folders:
        services = server1.services.list(folder=folder)
        for service in services:
            ii = service.iteminformation
            manifest = ii.manifest
            data_sources = manifest.get("databases", [])
        
            for data_source in data_sources:
                writer.writerow([service.properties.serviceName, data_sources])
