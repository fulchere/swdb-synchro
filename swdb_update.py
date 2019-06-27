#!/usr/bin/env python3
#
# Example usage of the Software Configuration DB API (aka SWDB) using CAS for authentication.
#
import sys
import json
import uuid

import os
import time
import datetime
import csv
import threading
from datetime import date
from pprint import pprint
from getpass import getpass


# Fix Jenkins missing imports
#sys.path.append(os.environ['WORKSPACE'])
import git
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
# (iocname, description, bool in database, swid, git urlname)
ioc_names_tuple_list = []
with open('ioc_names.csv') as csvfile:
    csvReader = csv.reader(csvfile)
    for row in csvReader:
        ls = [str(row[0]),str(row[1]),bool(row[2]),int(row[3]),str(row[4])]
        ioc_names_tuple_list.append(ls)
    
r2 = requests.get(SWDB_BASE_URL + '/api/v2/software', headers=headers)
r2_json = r2.json()
print()
for i in range(288):
    for tup in ioc_names_tuple_list:
        if r2_json['data'][i]['name'] == tup[0]:
            tup[2] = True
            tup[3] = r2_json['data'][i]['id']
            print("found",r2_json['data'][i]['name'],"ioc with id",r2_json['data'][i]['id'],"and engineer",r2_json['data'][i]['engineer'],"        ",end="\r")
print("\ndone updating local db\n")

#===================================================================================================================================
# Create SCDB entry

# threading function
def put_entry(sublist):
    for name_tuple in sublist:
        name = name_tuple[0]
        date_time = str(datetime.datetime.now())

        remote_refs = {}

        #os.environ['GIT_USERNAME'] = 'fulchere'
        g = git.cmd.Git()
        for ref in g.ls_remote("ssh://git@stash.frib.msu.edu:7999/diag/"+name_tuple[4]+".git").split('\n'):
            hash_ref_list = ref.split('\t')
            remote_refs[hash_ref_list[1]] = hash_ref_list[0]
        sha = remote_refs['refs/heads/release/fc2']
        
        if not name_tuple[2]:
            # is not there, create entry
            software = {
                'name': name,
                'desc': name_tuple[1],
                'owner': 'IFS:LAB.FRIB.ASD.BIM.ELECTRONICINSTRUMENTATION',
                'engineer': 'OMITTO',
                'branch': 'release/fc2',
                'version': str(sha),
                'status': 'RDY_TEST', # DEVEL, RDY_TEST, RDY_INST, DEP
                'statusDate': date_time[:10], 
                'levelOfCare': 'MEDIUM', # LOW, MEDIUM, HIGH
                'versionControl': 'GIT', # GIT, AC, FS, DEB, OTHER
                'versionControlLoc': '',
                'descDocLoc': '',
                'designDocLoc': '',
                'vvProcLoc': [],
                'vvResultsLoc': [],
                'platforms': 'linux (x86)',
                # "previous": "UUID"  # Previous version of this software (if available)
                'comment': 'This software entry created by script using SCDB API',
            }

            r = requests.post(SWDB_BASE_URL + '/api/v2/software', headers=headers, json={ 'data': software })
            if r.status_code != 201:
                print('Error creating software entry:', r.status_code, file=sys.stderr)
                pprint(r.json())
                sys.exit(1)

            pkg = r.json()
            swid = pkg['data']['id']
            print('Created entry with name:',name_tuple[0], 'and ID:', name_tuple[3])
            #pprint(pkg['data'])

        else:
            # is already there, update entry
            get = requests.get(SWDB_BASE_URL + '/api/v2/software/'+str(name_tuple[3]), headers=headers)
            pkg = get.json()
            pkg['data']['version'] = str(sha)
            pkg['data']['date'] = date_time[:10]
            pkg['data']['desc'] = str(name_tuple[1])
            pkg['data']['branch'] = 'release/fc2'

            r = requests.put(SWDB_BASE_URL + '/api/v2/software/'+name_tuple[3], headers=headers, json=pkg)
            if r.status_code != 200:
                print('Error updating software entry:', r.status_code, file=sys.stderr)
                pprint(r.json())
                sys.exit(1)

            print('updated entry with name:',name_tuple[0], 'and ID:', name_tuple[3], end="\n")
            #pprint(pkg['data'])

B = ioc_names_tuple_list[:len(ioc_names_tuple_list)//2]
B1 = B[:len(B)//2]
B2 = B[len(B)//2:]
C = ioc_names_tuple_list[len(ioc_names_tuple_list)//2:]
C1 = C[:len(C)//2]
C2 = C[len(C)//2:]
liss = [B1,B2,C1,C2]
t_ls = []
for i in range(4):
    thrd = threading.Thread(target=put_entry,args=(liss[i],))
    t_ls.append(thrd)
for t in t_ls:
    t.start()
for t in t_ls:
    t.join()
    

print("\ndone updating swdb")
print("\nSCRIPT EXECUTED SUCCESSFULLY")

