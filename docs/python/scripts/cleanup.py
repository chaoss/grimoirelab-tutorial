#! /usr/bin/env python3

import elasticsearch
from pprint import pprint

indexes = ['github_grimoirelab', 'git_grimoirelab',
        'github_grimoirelab-raw', 'git_grimoirelab-raw' ]

es = elasticsearch.Elasticsearch(['http://localhost:9200'])

aliases = es.indices.get_alias('*')
pprint(aliases)

all_schemas = es.indices.get('*')
for index in all_schemas.keys():
    print("Index: ", index)

for index in indexes:
    print("Removing index: ", index)
    es.indices.delete(index=index, ignore=[400, 404])

all_schemas = es.indices.get('*')
for index in all_schemas.keys():
    print("Index: ", index)

aliases = es.indices.get_alias('*')
pprint(aliases)
