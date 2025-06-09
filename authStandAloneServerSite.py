from arcgis.gis.server import Server

url = "https://server:6443/arcgis"
user = "username"
pwd = "password"

# connect to server with admin user
server = Server(url, username=user, password=pwd)

# get token to confirm succesfull login
token = server._con.relogin()
print(f"login token: {token}")
