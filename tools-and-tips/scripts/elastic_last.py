#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Copyright (C) 2016, 2017 Bitergia
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
import json
import logging
import operator
import time
import urllib3
import warnings

import elasticsearch
import elasticsearch_dsl

description = """Get latest items from ElasticSearch indexes.

Example:
    elastic_last metadata_updated_on http://elasctic.instance.xxx/index

"""

def parse_args ():

    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("urls", type=str, nargs='+',
                        help = "urls of the indexes to consider")
    parser.add_argument("--date_field", type=str,
                        default='metadata__timestamp',
                        help = "Date field for selecting latest items")
    parser.add_argument("--count", type=int, default=50,
                        help = "Number of items to get from each index")
    parser.add_argument("--total", type=int, default=40,
                        help = "Number of items to produce in total")


    parser.add_argument("--loop", type=int,
                        help = "Loop, refreshing data every loop seconds")
    parser.add_argument("--output", type=str,
                        default='events.json',
                        help = "Output file name")

    parser.add_argument("--verify_certs", dest="verify_certs",
                        action="store_true",
                        help = "Verify ssl certificates (default)")
    parser.add_argument("--no_verify_certs", dest="verify_certs",
                        action="store_false",
                        help = "Do not verify ssl certificates")
    parser.set_defaults(verify_certs=True)

    parser.add_argument("-l", "--logging", type=str,
                        choices=["warning", "info", "debug"],
                        help = "Logging level for output")
    parser.add_argument("--logfile", type=str,
                        help = "Log file")

    args = parser.parse_args()
    return args

def log_format (args):

    format = '%(levelname)s:%(message)s'
    if args.logging:
        if args.logging == "warning":
            level = logging.WARNING
        elif args.logging == "info":
            level = logging.INFO
        elif args.logging == "debug":
            level = logging.DEBUG
    else:
        level = logging.ERROR
        warnings.filterwarnings("ignore")
        # Disable warning about not verifying certificates
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if args.logfile:
        logging.basicConfig(format=format, level=level,
                            filename = args.logfile, filemode = "w")
    else:
        logging.basicConfig(format=format, level=level)

def last_items(url, verify_certs, date_field, count):
    """Get last items from index specified by url.

    """

    (es_url, index) = url.rsplit('/', 1)
    try:
        es = elasticsearch.Elasticsearch([es_url],
                                        verify_certs=verify_certs)
    except elasticsearch.exceptions.ImproperlyConfigured as exception:
        if exception.args[0].startswith("Root certificates are missing"):
            logging.error("Error validating SSL certificate for {}." \
                        .format(self.instance))
            logging.error("Use --no_verify_certs to avoid validation.")
            exit()
        else:
            raise
    request = elasticsearch_dsl.Search(using=es, index=index)
    request = request.sort('-' + date_field)
    request = request[0:count]
    try:
        response = request.execute()
    except elasticsearch.exceptions.RequestError as e:
        logging.error("Error fetching " + url)
        logging.error(e)
        exit()
    except:
        logging.error("Other exception caught")
        raise
    results = []
    for item in response:
        item['date'] = item[date_field]
        results.append(item.to_dict())
    return results

def main():
    args = parse_args()
    log_format(args)

    loop = True
    while loop:
        results = []
        for url in args.urls:
            results.extend(last_items(url, args.verify_certs,
                        args.date_field, args.count))
        sorted_results = sorted(results, key=operator.itemgetter(args.date_field))
        output_results = sorted_results[-args.total:]
        json_results = json.dumps(output_results, sort_keys=True, indent=2)
        with open(args.output, 'w') as f:
            f.write(json_results)
            print("Items read: ", len(sorted_results),
                "written: ", len(output_results))
        if args.loop:
            time.sleep(args.loop)
        else:
            loop = False

if __name__ == "__main__":
    main()
