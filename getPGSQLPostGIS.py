import arcpy
# path to connection file
sdeConnection = r"\(path\to\db.sde"
# set variable for sde file
conn = arcpy-ArcSDESQLExecute(sdeConnection)
# set variable for postgresql version and print result
pgSQLVer = conn.execute("SELECT Version;")
print(pgSQLVer)
# set variable for postGIS version and print result
postGISVer = conn. execute("SELECT PostGIS_Version();")
print(postGISVer)