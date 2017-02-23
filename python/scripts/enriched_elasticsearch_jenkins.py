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

import argparse
import datetime
import urllib3

import elasticsearch
import elasticsearch_dsl

description = """Produce CSV from some fields in a Jenkins enriched index"""

def parse_args ():

    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("--es", type=str, required=True,
                        help = "ElasticSearch instance")
    parser.add_argument("--es_index", type=str, required=True,
                        help = "ElasticSearch index with Jenkins data")
    parser.add_argument("--days", type=int, required=False,
                        default=90,
                        help = "ElasticSearch index with Jenkins data")
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

    es = elasticsearch.Elasticsearch([args.es],
                                    verify_certs=args.verify_certs)
    request = elasticsearch_dsl.Search(using=es,
                                        index=args.es_index)
    request = request.filter('range',
                        build_date={'from': datetime.datetime.now() - datetime.timedelta(days=args.days)})
    request = request.sort('-build_date')
    response = request.scan()

    print("job_build,build_date,duration(ms),result,builtOn,build,branch,loop,job_name")
    for job in response:
        print("{},{},{},{},{},{},{},{},{}".format(
                job['job_build'], job['build_date'],
                job['duration'], job['result'],
                job['builtOn'], job['build'],
                job['branch'], job['loop'], job['job_name']
                ))

if __name__ == "__main__":
    main()
