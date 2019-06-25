#!/usr/bin/env python3
#
# Example usage of the Software Configuration DB API (aka SWDB) using CAS for authentication.
#
import sys
import json
import uuid
import git
import os
import shutil
import time
import datetime
from datetime import date
from pprint import pprint
from getpass import getpass


import requests

# Consider using the Requests-OAuthlib libary

### CAS_BASE_URL = 'https://cas3.nscl.msu.edu/cas'
CAS_BASE_URL = 'https://cas3-dev.nscl.msu.edu/cas'

### SWDB_BASE_URL = 'https://controls.frib.msu.edu/swdb'
SWDB_BASE_URL = 'https://controls-dev.frib.msu.edu/swdb'

print("Enter OAuth2 client credentials")
client_id = "FULCHER" #client_id = input("client_id: ")
client_secret = "lZjckorQMK9+7BDTYpqGL+fWIGSNmEWUm5jt2nJ9ncULfTfc4AEdpdEmYxvLS4QC" #client_secret = getpass("client_secret: ")

# Request an OAuth 2.0 Access Token
r = requests.post(CAS_BASE_URL + '/oauth2.0/accessToken',
    headers={
        'Accept':'application/json',
    },
    data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    },
)

if r.status_code != 200:
    print('Authentication failed:', client_id, file=sys.stderr)
    print(r.text)
    sys.exit(1)

data = r.json()
token_type = data['token_type'] # type should always be 'Bearer'
access_token = data['access_token']
print('Access token:', access_token)
print('Access expires in:', data['expires_in'], 'seconds')

headers = {
    'Accept':'application/json',
    'Content-Type': 'application/json',
    'Authorization': token_type + ' ' + access_token,
}

#====================================================================================================================================
# (iocname, description, bool in database, swid)
ioc_names_tuple_list = [["autocalib","Automatic Calibration IOC", False, -1], ["bcm_struck_ioc", "BCM IOC", False, -1], ["bcm_enable", "BCM Enable IOC", False, -1], ["bcm_report", "BCM Report IOC", False, -1], ["bpm", "BPM IOC", False, -1], ["bpm-archiver-tool", "BPM Archiver Data IOC", False, -1],  ["chargesel", "Charge Selector IOC", False, -1], ["mtca_evr", "EVR IOC", False, -1], ["fths", "FTHS IOC", False, -1], ["galilrio", "Galil IOC", False, -1], ["diag_genavg", "Genavg IOC", False, -1], ["diag_health", "Diagnostics Health IOC", False, -1], ["ic-ioc", "Ion Chamber IOC", False, -1], ["mtca_ipmi", "IPMI IOC", False, -1], ["motor-maintenance", "Motor Maintenance IOC", False, -1], ["nd-ioc", "Neutron Detector IOC", False, -1], ["ndwarp", "Camera IOC", False, -1], ["pfmScan", "Profile Monitor IOC", False, -1], ["restore", "Restore IOC", False, -1], ["scan02", "Allison Scanner IOC", False, -1], ["statusUtil", "Diagnostics Status IOC", False, -1], ["stopCam", "Stop Camera IOC", False, -1], ["tpmacioc", "Motor Controller IOC", False, -1], ["wfgather", "Waveform Gathering IOC", False, -1]]
# ["bpmenergy", "BPM Energy IOC", False, -1],
r2 = requests.get(SWDB_BASE_URL + '/api/v2/software', headers=headers)
r2_json = r2.json()
print()
for i in range(283):
    for tup in ioc_names_tuple_list:
        if r2_json['data'][i]['name'] == tup[0]:
            tup[2] = True
            tup[3] = r2_json['data'][i]['id']
            print("found",r2_json['data'][i]['name'],"ioc with id",r2_json['data'][i]['id'],"and engineer",r2_json['data'][i]['engineer'],end="\n")
print("done updating local db\ndeleting entries in swdb\n")

for name_tuple in ioc_names_tuple_list:
    if name_tuple[2]:
        deleted = requests.delete(SWDB_BASE_URL + '/api/v2/software/'+str(name_tuple[3]), headers=headers)
        if deleted.status_code != 200:
            print('Error deleting software entry:', deleted.status_code, file=sys.stderr)
            pprint(deleted.json())
            sys.exit(1)
        print("deleted entry with name:",name_tuple[0],"and id:", name_tuple[3])

