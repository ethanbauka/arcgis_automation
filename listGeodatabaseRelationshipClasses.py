import arcpy
from arcpy import env

workspace = env.workspace = r"path to file geodatabase or .sde connection file here"

rc_list = [c.name for c in arcpy.Describe(workspace).children if c.datatype == "RelationshipClass"]

# this for loop will list the names and origin primary and foreign keys of the relationship classes in the geodatabase
for rc in rc_list:
    rc_path = workspace + "\\" + rc
    des_rc = arcpy.Describe(rc_path)
    key = des_rc.originClassKeys
    print(rc)
    print(key)

# this for loop will list the names, origin, and destination of the relationship classes in the geodatabase
for rc in rc_list: 
    rc_path = workspace + "\\" + rc 
    des_rc = arcpy.Describe(rc_path) 
    origin = des_rc.originClassNames 
    destination = des_rc.destinationClassNames 
    print ("Relationship Class: %s \n Origin: %s \n Desintation: %s" %(rc, origin, destination))
