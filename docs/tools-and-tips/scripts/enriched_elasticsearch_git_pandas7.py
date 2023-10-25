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
## Some simple examples about how to query enriched indexes using
## elasticsearch_dsl

import argparse
from datetime import datetime
from pprint import pprint
import urllib3

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A
from elasticsearch_dsl import Mapping, String, Date
import elasticsearch.helpers

import pandas as pd

description = "Produce CSV files with new authors"

new_file = 'new_authors_orgs_repo.csv'

def parse_args ():

    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("--es", type=str, required=True,
                        help = "ElasticSearch instance to read")
    parser.add_argument("--es_index", type=str, required=True,
                        help = "ElasticSearch index with data to read")
    parser.add_argument("--es_out", type=str, required=True,
                        help = "ElasticSearch instance to write" \
                            + " (default: es)")
    parser.add_argument("--es_index_out", type=str, required=True,
                        help = "ElasticSearch index to write data")
    parser.add_argument("--verify_certs", dest="verify_certs",
                        action="store_true",
                        help = "Verify ssl certificates")
    parser.add_argument("--no_verify_certs", dest="verify_certs",
                        action="store_false",
                        help = "Do not verify ssl certificates")
    parser.set_defaults(verify_certs=True)
    args = parser.parse_args()
    return args

def main():
    # Disable warning about not verifying certificates
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    args = parse_args()
    es = Elasticsearch([args.es],
                        verify_certs=args.verify_certs,
                        timeout=35)
    if args.es_out:
        es_out = Elasticsearch([args.es_out],
                        verify_certs=args.verify_certs,
                        timeout=35)
    else:
        es_out = es

    es_index = args.es_index
    es_index_out = args.es_index_out

    def get_authors(es, es_index):

        # Buckets by author name, finding first commit for each of them
        s = Search(using=es, index=es_index)
        s.aggs.bucket('by_authors', 'terms', field='author_name', size=0) \
            .bucket('repos', 'terms', field='repo_name', size=0) \
            .metric('first', 'top_hits',
                _source=['author_date', 'author_org_name',
                    'author_uuid', 'project'],
                size=1, sort=[{"author_date": {"order": "asc"}}]) \
            .metric('last_commit', 'max', field='author_date') \
            .metric('commits', 'cardinality', field='hash')
        s = s.sort("author_date")
#       pprint(s.to_dict())
        result = s.execute()

#       pprint(result.to_dict())
        # Get a dataframe with each author and their first commit
        buckets_result = result['aggregations']['by_authors']['buckets']
#       pprint(buckets_result)
        buckets = []
        for bucket_author in buckets_result:
            author = bucket_author['key']
            for bucket_repo in bucket_author['repos']['buckets']:
                first = bucket_repo['first']['hits']['hits'][0]
                first_commit = first['sort'][0]/1000
                last_commit = bucket_repo['last_commit']['value']/1000
                commits = bucket_repo['commits']['value']
                org_name = first['_source']['author_org_name']
                project = first['_source']['project']
                uuid = first['_source']['author_uuid']
                buckets.append(
                    {'first_commit': datetime.utcfromtimestamp(first_commit),
                    'last_commit': datetime.utcfromtimestamp(last_commit),
                    'author_name': author,
                    'commits': commits,
                    'uuid': uuid,
                    'author_org_name': org_name,
                    'repo_name': bucket_repo['key'],
                    'project': project}
                )
        authors_repos = pd.DataFrame.from_records(buckets)
#        pprint(authors_repos)
        authors_repos.sort_values(by='first_commit', ascending=False,
                                inplace=True)
        return(authors_repos)

    authors_repos = get_authors(es, es_index)
    authors = authors_repos.groupby('author_name').last().reset_index()
    authors.sort_values(by='first_commit', ascending=False,
                        inplace=True)

    print("Creating CSV for first date for authors: " + new_file)
    authors.to_csv(new_file,
                columns=['first_commit', 'last_commit', 'author_name', 'commits', 'author_org_name', 'repo_name', 'project'],
                index=False)

    def mapping_es (es, es_index):

        mapping = Mapping('items')
        mapping.field('author_name', String(index='not_analyzed'))
        mapping.field('first_commit', Date())
        mapping.field('last_commit', Date())
        mapping.field('commits', 'integer')
        mapping.field('author_org_name', String(index='not_analyzed'))
        mapping.field('repo_name', String(index='not_analyzed'))
        mapping.field('project', String(index='not_analyzed'))
        mapping.field('uuid', String(index='not_analyzed'))
        print("Uploading mapping to ElasticSearch")
        mapping.save(es_index, using=es)

    def upload_es (es, es_index, df, columns):

        es_type = 'items'
        actions = []
        for row in df[columns].to_dict(orient='records'):
            to_write = {
                '_op_type': 'index',
                '_index': es_index,
                '_type': es_type,
                '_id': row['uuid'],
            }
            to_write.update(row)
            actions.append(to_write)
        print("Uploading to ElasticSearch")
        elasticsearch.helpers.bulk(es, actions)

    mapping_es(es_out, es_index_out)
    upload_es(es_out, es_index_out, authors,
                ['first_commit', 'last_commit', 'author_name', 'uuid',
                'commits', 'author_org_name', 'repo_name', 'project'])

if __name__ == "__main__":
    main()
