# code from esri for automating moving custom roles from one portal to another

from arcgis.gis import GIS, RoleManager
import json
import argparse
import datetime
import logging
import os
import time
 
 
# setup logger
def get_logger(log_name, log_dir, run_name):
    the_logger = logging.getLogger(run_name)
    the_logger.setLevel(logging.INFO)
 
    # Ensure Directories Exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
 
    # Set Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
 
    # Set File Handler
    fh = logging.FileHandler(os.path.join(log_dir, log_name), 'a')
    fh.setLevel(logging.info)
 
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
 
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
 
    the_logger.addHandler(ch)
    the_logger.addHandler(fh)
 
    the_logger.info('Logger Initialized')
 
    return the_logger
 
 
def read_json_file(filepath):
    with open(filepath) as json_file:
        data = json.load(json_file)
 
    return data
 
 
if __name__ in "__main__":
 
    # setup the arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--portal_customizations_config_file', help='Path to the portal customizations config file')
 
    # gather the arguments
    args = parser.parse_args()
    ps_config_json_file = args.portal_customizations_config_file
 
    # Get Start Time
    start_time = time.time()
 
    # Get Script Directory
    this_dir = os.path.split(os.path.realpath(__file__))[0]
 
    # Get Logger
    t_format = datetime.datetime.fromtimestamp(start_time).strftime('%d_%m_%H_%M_%S')
    log_name = f'portal-customizations-run_{t_format}.log'
    # log_dir = os.path.join(this_dir, 'logs')
    # logger = get_logger(log_name, log_dir, 'LOGGER')
 
    dn = os.path.dirname(os.path.realpath(__file__))
    logFile = os.path.join(dn,"python.log")
    logging.basicConfig( filename = logFile,filemode = 'a',level = logging.INFO,format = '%(asctime)s -- %(levelname)s -- %(message)s',datefmt = '%Y-%m-%d_%I:%M:%S'  )
 
    # read in the config file
    ps_config_json = read_json_file(ps_config_json_file)
 
    # parse the variables from the config files
    source_username = ps_config_json['source_username']
    source_password = ps_config_json['source_password']
    source_fqdn = ps_config_json['source_fqdn']
    source_portal_context = ps_config_json['source_portal_context']
    source_url = f"https://{source_fqdn}/{source_portal_context}"
 
    target_username = ps_config_json['target_username']
    target_password = ps_config_json['target_password']
    target_fqdn = ps_config_json['target_fqdn']
    target_portal_context = ps_config_json['target_portal_context']
    target_url = f"https://{target_fqdn}/{target_portal_context}"
 
    logging.info("----------------------------- Starting Python Script -----------------------------")
    logging.info('Creating GIS and RoleManager objects...')
    # create the GIS object
    source_gis = GIS(source_url, source_username, source_password, verify_cert=False)
    target_gis = GIS(target_url, target_username, target_password, verify_cert=False)
    # create the role manager object
    source_rm = RoleManager(source_gis)
 
    # Create custom roles and ignore the default roles
    default_roles = ["Administrator", "Data Editor", "Publisher", "User", "Viewer"]
 
    for role in source_rm.all():
        if role.name in default_roles:
            logging.info(f"Skipping default role: {role.name}")
        else:
            logging.info("Retrieving source role name, description, and privileges...")
            role_name=role.name
            role_id = role.role_id
            role_description = role.description
            role_privs = role.privileges
            logging.info("Successfully retrieved source role name, description, and privileges.")
 
            # create exact role in target environment
            logging.info(f"Creating new role {role.name}")
            new_target_role = target_gis.users.roles.create(name=role_name,
                                                            description=role_description,
                                                            privileges=role_privs)
            if new_target_role:
                logging.info(f"Created new role {role.name} in target enviornment.")
                logging.info(f"Source Role ID: {role_id}")
                logging.info(f"Target Role ID: {new_target_role.role_id}")
            else:
                logging.info(f"There was an error creating the role named {role.name} in the target environment.")
 
    logging.info("----------------------------- Python Script Completed -----------------------------")
