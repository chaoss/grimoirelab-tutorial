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

# Build a DSL Search object on the 'git' index, 'summary' documents type
request = elasticsearch_dsl.Search(using=es, index='commits',
                                    doc_type='summary')
# We need to request only some fields
request = request.source(['hash', 'author_date', 'author'])

# Run the Search, using the scan interface to get all resuls
response = request.scan()
for commit in response:
    print(commit.hash, commit.author_date, commit.author)
