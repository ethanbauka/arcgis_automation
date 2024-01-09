import arcpy
import os
import sys

file = open(r"C:\\getCount.txt", "w")
sys.stdout = file

# Input your workspace (this will also work for a folder path containing multiple geodatabases)
workspace = r"Database Connections\\insertDatabaseNameHere.sde"

# Get a list of all the feature classes and tables in the workspace
feature_classes = []
walk = arcpy.da.Walk(workspace, datatype= ["FeatureClass", "Table"])

for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        feature_classes.append(os.path.join(dirpath, filename))

# Get counts and add to a dictionary
d = {}
for fc in feature_classes:
    count = arcpy.GetCount_management(fc)
    d[os.path.basename(fc)] = int(count[0])

# Print feature classes and their feature (row) count
print('\n'.join("{} = {} RECORDS".format(k, v) for k, v in d.items()))

# Get a total count of all rows
print("TOTAL RECORDS IN DATABASE = {0}".format(sum(d.values())))

file.close()
