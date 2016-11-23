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

import email.utils

import perceval.backends
import elasticsearch

# uri (label) for the mailing list to analyze
mbox_uri = 'http://mail-archives.apache.org/mod_mbox/httpd-announce/'
# directory for letting Perceval where mbox archives are
# you need to have the archives to analyzed there before running the script
mbox_dir = 'archives'
# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Create the 'messages' index in ElasticSearch
try:
    es.indices.create('messages')
except elasticsearch.exceptions.RequestError:
    print('Index already exisits, remove it before running this script again.')
    exit()

# create a mbox object, using mbox_uri as label, mbox_dir as directory to scan
repo = perceval.backends.mbox.MBox(uri=mbox_uri, dirpath=mbox_dir)

# Fetch all commits as an iteratoir, and iterate it uploading to ElasticSearch
print('Analyzing mbox archives...')
# fetch all messages as an iteratoir
for message in repo.fetch():
    # Create the object (dictionary) to upload to ElasticSearch
    summary = {
        'from': message['data']['From'],
        'subject': message['data']['Subject'],
        'date': email.utils.parsedate_to_datetime(message['data']['Date'])
        }
    print('.', end='')
    # Upload the object to ElasticSearch
    es.index(index='messages', doc_type='summary', body=summary)

print('\nCreated new index with commits.')
