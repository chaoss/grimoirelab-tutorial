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
## Some simple examples about how to query enriched indexes using
## elasticsearch_dsl

from datetime import datetime
from pprint import pprint

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


es = Elasticsearch(["http://127.0.0.1:9200"])
index = 'git'

# Counting total number of commits
s = Search(using=es, index=index)
total = s.count()
print("Count of total number of commits in index: ", total)

# Counting number of unique commits
s = Search(using=es, index=index)
s.aggs.metric('commits', 'cardinality', field='hash')
unique = s.count()
print("Count of unique commits in index: ", unique)

# Counting number of unique commits, ignoring those touching no files
s = Search(using=es, index=index)
s = s.filter('range', files={'gt':0})
s.aggs.metric('commits', 'cardinality', field='hash')
unique_no_empty = s.count()
print("Count of unique commits in index: ", unique_no_empty)

# Counting number of unique commits, ignoring those touching no files
# and newer than a date
s = Search(using=es, index=index)
s = s.filter('range', files={'gt':0})
s = s.filter('range', author_date={'gt': datetime(2016, 7, 1)})
s.aggs.metric('commits', 'cardinality', field='hash')
unique_after = s.count()
print("Count of unique commits in index, authored later than July 1st 2016: ",
 unique_after)

# Counting number of unique commits, ignoring those touching no files
# and newer than a date, grouping by quarter
s = Search(using=es, index=index)
s = s.filter('range', files={'gt':0})
s = s.filter('range', author_date={'gt': datetime(2016, 7, 1)})
s.aggs.metric('commits', 'cardinality', field='hash')
s.aggs.bucket('histogram', 'date_histogram',
    field='author_date', interval='quarter')
by_quarter = s.execute()
print("Aggregations returned by quarter")
pprint(by_quarter.to_dict()['aggregations'])
for quarter in by_quarter.to_dict()['aggregations']['histogram']['buckets']:
    print("Unique commits for quarter starting on ",
        quarter['key_as_string'],
        ": ", quarter['doc_count'])
