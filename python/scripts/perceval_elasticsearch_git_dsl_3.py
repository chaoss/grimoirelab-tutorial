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

import elasticsearch
import elasticsearch_dsl

# ElasticSearch instance (url)
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# Build a DSL Search object on the 'commits' index, 'summary' documents type
request = elasticsearch_dsl.Search(using=es, index='commits',
                                    doc_type='summary')
# We want the last 20 commits, by commit timestamp, with only some fields
request = request.sort('-commit_date')
request = request.source(['hash', 'author_date', 'author'])
request = request[0:20]

# Run the Search, using the execute interface to get ordered results
response = request.execute()
for commit in response:
    print(commit.hash, commit.author_date, commit.author)
