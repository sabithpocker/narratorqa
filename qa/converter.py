import json
from datetime import datetime
from dateutil.parser import parse

nodes = []
catalogs = []
count = 1
with open('items_catalogspider_1-2.json') as data_file:    
    data = json.load(data_file)

for catalog in data:
    catalog['pk'] = count
    count = count + 1
    for node in catalog['nodes']:
        node['catalog'] = catalog['pk']
        nodes.append(node)
    del catalog['nodes']
    del catalog['_type']
    catalogs.append(catalog)

for index, node in enumerate(nodes):
    node['pk'] = index + 1
    node['model'] = 'data.node'
    node['fields'] = {}
    node['fields']['catalog'] = node['catalog']
    del node['catalog']
    node['fields']['title'] = node['title']
    del node['title']
    node['fields']['node'] = node['node']
    del node['node']
    node['fields']['url'] = node['url']
    del node['url']

for catalog in catalogs:
    catalog['model'] = 'data.catalog'
    catalog['fields'] = {}
    catalog['fields']["title"]= catalog['title']
    del catalog['title']
    catalog['fields']["description"]= catalog['description']
    del catalog['description']
    catalog['fields']["ministry_department"]= catalog['ministry_department']
    del catalog['ministry_department']
    catalog['fields']["state_department"]= catalog['state_department']
    del catalog['state_department']
    catalog['fields']["data_sets_actual_count"]= catalog['data_sets_actual_count']
    del catalog['data_sets_actual_count']
    catalog['fields']["data_sets_count"]= catalog['data_sets_count']
    del catalog['data_sets_count']
    catalog['fields']["last_updated"]= datetime.strptime(catalog['last_updated'], '%d/%m/%y').isoformat()
    del catalog['last_updated']
    catalog['fields']["url"]= catalog['url']
    del catalog['url']

with open("converted.json", "w") as jsonFile:
    json.dump(catalogs + nodes, jsonFile, indent=2)
