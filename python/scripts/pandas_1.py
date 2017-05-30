#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Copyright (C) 2017 Bitergia
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
## Some simple examples for exploring how to work with pandas
## and GrimoireLab indexes.

from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd

es_url = 'http://localhost:9200'
es_index = 'git'

es = Elasticsearch(es_url, verify_certs=False)

# Buckets by author name, finding first commit for each of them
s = Search(using=es, index=es_index)
s.aggs.bucket('by_authors', 'terms', field='author_name', size=10000) \
    .metric('first_commit', 'min', field='author_date')
s = s.sort("author_date")
result = s.execute()

# Get a dataframe with each author and their first commit
buckets_result = result['aggregations']['by_authors']['buckets']
buckets = []
for bucket in buckets_result:
    first_commit = bucket['first_commit']['value']/1000
    buckets.append(
        {'first_commit': datetime.utcfromtimestamp(first_commit),
        'author': bucket['key']}
        )
authors = pd.DataFrame.from_records(buckets)
authors.sort_values(by='first_commit', ascending=False, inplace=True)

# Get number of new authors per month
by_month = authors['first_commit'] \
    .groupby([authors.first_commit.dt.year,
            authors.first_commit.dt.month]) \
    .agg('count')

# Produce csv files
print("Creating CSV for new authors per month.")
by_month.to_csv('authors_per_month.csv')
print("Creating CSV for first date for authors.")
authors.to_csv('authors_first.csv',
                columns=['first_commit', 'author'],
                index=False)
