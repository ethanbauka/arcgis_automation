import os
import arcpy
from arcpy import sharing
from arcgis.gis import GIS
from arcgis.layers import _service_factory
from tkinter import simpledialog

gis = GIS("pro")
print(gis)

items = gis.content.search(
  query=f"owner:{gis.users.me.username}",
  item_type='Map Service'
)

index = simpledialog.askinteger(
  "Service Selection:",
  "Select service index:\n{}".format(
    "\n".join((f"[{i}] : {v}" for i,v in enumerate(items)))
  )
)

privateUrl = items[index].privateUrl
print(privateUrl)
service = _service_factory.Service(privateUrl,gis)
service.service.stop()

outdir = "path to out dir"
service_name = items[index].title
sddraft_filename = service_name + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)
sd_filename = service_name + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)
print(sd_output_filename)

