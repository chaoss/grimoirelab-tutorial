#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Copyright (C) 2016 Bitergia
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
##
## Authors:
##   Jesus M. Gonzalez-Barahona <jgb@bitergia.com>
##

import datetime

from perceval.backends.core.git import Git
import elasticsearch

# Url for the git repo to analyze
repo_url = 'http://github.com/grimoirelab/perceval.git'
# Directory for letting Perceval clone the git repo
repo_dir = '/tmp/perceval.git'
# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Create the 'commits' index in ElasticSearch
try:
    es.indices.create('commits')
except elasticsearch.exceptions.RequestError:
    print('Index already exisits, remove it before running this script again.')
    exit()
# Create a Git object, pointing to repo_url, using repo_dir for cloning
repo = Git(uri=repo_url, gitpath=repo_dir)
# Fetch all commits as an iteratoir, and iterate it uploading to ElasticSearch
print('Analyzing git repo...')
for commit in repo.fetch():
    # Create the object (dictionary) to upload to ElasticSearch
    summary = {
        'hash': commit['data']['commit'],
        'author': commit['data']['Author'],
        'author_date': datetime.datetime.strptime(commit['data']['AuthorDate'],
                                                "%a %b %d %H:%M:%S %Y %z"),
        'commit': commit['data']['Commit'],
        'commit_date': datetime.datetime.strptime(commit['data']['CommitDate'],
                                                "%a %b %d %H:%M:%S %Y %z"),
        'files_no': len(commit['data']['files'])
        }
    print('.', end='')
    # Upload the object to ElasticSearch
    es.index(index='commits', doc_type='summary', body=summary)

print('\nCreated new index with commits.')
