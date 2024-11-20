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

aprx = arcpy.mp.ArcGISProject("path to .aprx")
federated_server_url = "url of federated server"
sddraft = m.getWebLayerSharingDraft(server_type, "MAP_IMAGE", service_name)
sddraft.federatedServerUrl = federated_suerver_url
sddraft.extension.feature.isEnabled = True
sddraft.extension.feature.featureCapabilities = "Query,Create,Update,Delete,Extract,Editing"
sddraft.overwriteExistingService = True

sddraft.exportToSDDraft(sddraft_output_filename)
arcpy.server.StageService(sddraft_output_filename, sd_output_filename, 102)
arcpy.server.UploadServiceDefintion(sd_output_filename, federated_server_url)

service.service.start()
print("View Map Service:", privateUrl)
