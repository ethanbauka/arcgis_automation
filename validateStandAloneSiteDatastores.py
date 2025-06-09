# import libraries
from arcgis.gis import GIS
from arcgis.gis.server import Server
from getpass import getpass

# create list of server sites or machines
server_sites = [
    {"url": "https://arcgisservermachine1.com:6443/arcgis"},
    {"url": "https://arcgisservermachine2.com:6443/arcgis"}
]

# loop through each server site
for server_site in server_sites:
    server_url = server_site["url"]
    print(server_url)
    user = getpass("Username: ")
    pwd = getpass("Password: ")
    
    # connect to server as admin
    server = Server(server_url, username=user, password=pwd)
    
    # relogin and get token to confirm successfull login
    token = server._con.relogin()
    print(f"login token: {token}")
    
    # get list of datastores on the server
    dstores = server.datastores.list()
    
    # loop through datastores and validate them
    for dstore in dstores:
        try:
            print(dstore.properties.path)
            print(dstore.validate())
        except:
            print('False')

print("script complete")
