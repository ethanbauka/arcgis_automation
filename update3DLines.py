"""
This script will update the z vertices (geometry) of lines
using an associated point layer.

"""

import arcpy

# Get the current project
project = arcpy.mp.ArcGISProject("CURRENT")

# Get the active map
active_map = project.activeMap

# Define the line layer and point layer
line_layer = active_map.listLayers("line_layer")[0]
point_layer = active_map.listLayers("point_layer")[0]

# Create a dictionary to store X, Y and Z values from the point layer (use the Elevation field for the z values)
point_dict = {(row[0], row[1]): row[2] for row in arcpy.da.SearchCursor(point_layer, ["SHAPE@X", "SHAPE@Y", "Elevation"])}

# Start an update cursor on the line layer
with arcpy.da.UpdateCursor(line_layer, ["SHAPE@"]) as cursor:
    for row in cursor:
        # Get the line geometry
        line_geom = row[0]
        
        # Create a new array to store the updated vertices
        new_part = arcpy.Array()
        
        # Update the Z vertices of the line
        for part in line_geom:
            for vertex in part:
                # Create a tuple of X and Y coordinates of the vertex
                xy = (vertex.X, vertex.Y)
                
                # Check if the vertex's X and Y coordinates exist in the point dictionary
                if xy in point_dict:
                    # Get the new Z value from the point dictionary
                    new_z = point_dict[xy]
                    
                    # Create a new point with the updated Z value
                    new_vertex = arcpy.Point(vertex.X, vertex.Y, new_z)
                    new_part.add(new_vertex)
                else:
                    # If the vertex's X and Y coordinates do not exist in the point dictionary, keep the original vertex
                    new_part.add(vertex)
        
        # Create a new Polyline object with the updated vertices
        new_line = arcpy.Polyline(new_part, line_geom.spatialReference, True)
        
        # Update the line geometry in the layer
        row[0] = new_line
        
        # Update the row
        cursor.updateRow(row)

print("Update completed.")
