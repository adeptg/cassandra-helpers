#!/usr/bin/env python3

import os
import re
import subprocess

HINTS_DIR = '/var/lib/cassandra/hints/'

hists_dict = {}
hists_dict_names = {}

with os.scandir(HINTS_DIR) as entries:
    for entry in entries:
        if not entry.name.endswith('.hints'):
            continue
        node_id = '-'.join(entry.name.split('-')[:5])
        if node_id not in hists_dict:
            hists_dict[node_id] = 1
        else:
            hists_dict[node_id] += 1

nodetool_status_process = subprocess.run(["nodetool","status"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
nodetool_status = nodetool_status_process.stdout

for id in hists_dict:
    if re.search(id,nodetool_status):
        #Node name found        
        node_name = re.search(id+"\s+(\S+)\n",nodetool_status).group(1)
        hists_dict_names[node_name] = hists_dict[id]
    else:
        hists_dict_names[id] = hists_dict[id]
        
print(sorted(hists_dict_names.items(), key=lambda x: x[1], reverse = True))
    

