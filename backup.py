# Copyright (c) 2017 Alex Kramer, Cat Tech <1336gm2@follett.com>
# See the LICENSE.txt file at the top-level of this distribution.

import requests
import json
import os
import sys
import logging

from datetime import datetime

# Read in JSON configuration file location
try:
    config_fname = str(sys.argv[1])
except IndexError as err:
    err_message = "Configuration file path is a required argument."
    raise IndexError(err_message) from err

# Check for configuration file
try:
    config_file = open(config_fname, "r")
except FileNotFoundError as err:
    err_message = "Specified configuration file not found."
    raise FileNotFoundError(err_message) from err

# Parse configuration file
config_dict = json.load(config_file)
config_file.close()

# Get configuration parameters
try:
    fs_domain = config_dict["domain"]
    fs_key = config_dict["api_key"]
    backup_path = config_dict["backup_path"]
    backup_fmt = config_dict["backup_format"]
    json_indent = config_dict.get("json_indent", None)
except KeyError as err:
    err_message = "Required configuration file key(s) missing"
    raise KeyError(err_message) from err

# Ensure backup path exists
try:
    backup_path = os.path.abspath(backup_path) + "/"
    os.system("mkdir -p " + backup_path)
except OSError as err:
    err_message = "Backup path does not exist and / or cannot be created"
    raise OSError(err_message) from err

# Open backup file / log
backup_fname = datetime.utcnow().strftime(backup_fmt)
backup_json_fname  = backup_fname + ".json"
backup_log_fname = backup_fname + ".log"
backup_json_file = open(backup_path + backup_json_fname, "w")

# Start logger
logging.basicConfig(filename=backup_path + backup_log_fname, level=logging.INFO)

logging.info("Configurable parameters:")
logging.info("FreshService domain: " + fs_domain)
logging.info("FreshService API Key: " + fs_key)
logging.info("Backup path: " + backup_path)
logging.info("Backup datetime format string: " + backup_fmt)
logging.info("JSON indent level: " + str(json_indent))

# Get a full backup of all tickets by iterating through paginated ticket lists
ticket_url = fs_domain + "/helpdesk/tickets/filter/all_tickets?format=json"
ticket_list = list()

logging.info("Starting data scrape from FreshService API")
page_num = 1
more_pages = True
while more_pages:
    req_url = ticket_url + "&page=" + str(page_num)
    logging.info("Requesting " + str(req_url))
    ticket_page_req = requests.get(req_url, auth=(fs_key, ""))

    # Check request HTTP status code
    status_code = ticket_page_req.status_code
    if (status_code != 200):
        err_message = "Incorrect status code: " + str(status_code) + \
                      "for request to URL: " + req_url
        logging.error(err_message)
        raise requests.exceptions.HTTPError(err_message)

    # Get JSON list of tickets from request
    ticket_page_json = ticket_page_req.json()

    # Check number of tickets in page, if page is blank, we've reached the end
    # of the tickets
    ticket_page_len = len(ticket_page_json)
    if (ticket_page_len > 0):
        ticket_list = ticket_list + ticket_page_json
        page_num += 1
    else:
        logging.info("Completed data scrape at ticket page " + str(page_num))
        logging.info("Total number of tickets: " + str(len(ticket_list)))
        more_pages = False

# Write backup to file
logging.info("Dumping scraped JSON data to " + backup_json_fname)
json.dump(ticket_list, backup_json_file, sort_keys=True, indent=json_indent)
logging.info("Backup complete, exiting.")

backup_json_file.close()
