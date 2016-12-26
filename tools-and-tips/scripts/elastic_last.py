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

import argparse
import json
import logging
import operator
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
    parser.add_argument("field", type=str,
                        help = "Date field for selecting latest items")
    parser.add_argument("urls", type=str, nargs='+',
                        help = "urls of the indexes to consider")
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

def main():
    args = parse_args()
    log_format(args)

    results = []
    for url in args.urls:
        (es_url, index) = url.rsplit('/', 1)
        try:
            es = elasticsearch.Elasticsearch([es_url],
                                            verify_certs=args.verify_certs)
        except elasticsearch.exceptions.ImproperlyConfigured as exception:
            if exception.args[0].startswith("Root certificates are missing"):
                logging.error("Error validating SSL certificate for {}." \
                            .format(self.instance))
                logging.error("Use --no_verify_certs to avoid validation.")
                continue
            else:
                raise
        request = elasticsearch_dsl.Search(using=es, index=index)
        request = request.sort('-' + args.field)
        request = request[0:20]
        try:
            response = request.execute()
        except elasticsearch.exceptions.RequestError as e:
            logging.error("Error fetching " + url)
            logging.error(e)
            continue
        except:
            logging.error("Other exception caught")
        for item in response:
            results.append(item.to_dict())
    sorted_results = sorted(results, key=operator.itemgetter(args.field))
    json_results = json.dumps(sorted_results, sort_keys=True, indent=2)
    print(json_results)

if __name__ == "__main__":
    main()
