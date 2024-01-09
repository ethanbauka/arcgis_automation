import arcpy

arcpy.env.overwriteOutput = True

# Variables for source and replica databases:
sourceData = r"Database Connections\\sourceData.sde\\source.GISa.featureClassNameHere"
replica = r"Database Connections\\replica.sde\\replica.DBO.featureClassNameHere"

# Get counts for the source and replica data before appending
print("source total rows = " , arcpy.GetCount_management(sourceData))
print("replica total rows = " , arcpy.GetCount_management(replica))

# Delete Rows of replica data and append the source data
# Note: this works best if the schemas match
arcpy.DeleteRows_management(replica)
print("replica total rows after deletion = " , arcpy.GetCount_management(replica))
arcpy.Append_management(sourceData, replica, "NO_TEST")
print("The total number of rows in the replica after the append = " , arcpy.GetCount_management(replica))
