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
import urllib3

import elasticsearch
import elasticsearch.helpers

description = """Copy data between ElasticSearch instances and files.

Example:
    elastic_cp --src http://elasctic.instance.xxx --src_index index \
        --dest dest_file.json

"""

# Disable warning about not verifying certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_args ():

    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("-l", "--logging", type=str, choices=["info", "debug"],
                        help = "Logging level for output")
    parser.add_argument("--logfile", type=str,
                            help = "Log file")
    parser.add_argument("--src", type=str, required=True,
                        help = "Data source (file path or ElasticSearch url)")
    parser.add_argument("--dest", type=str, required=True,
                        help = "Data sink (file path or ElasticSearch url)")
    parser.add_argument("--src_index", type=str,
                        help = "Source index (for ElasticSearch as data source)")
    parser.add_argument("--dest_index", type=str,
                        help = "Sink index (for ElasticSearch as data sink)")
    parser.add_argument("--match", type=str, nargs=2,
                        help = "Consider only documents with field value (only for ElasticSearch)")
    parser.add_argument("--verify_certs", dest="verify_certs",
                        action="store_true",
                        help = "Verify ssl certificates")
    parser.add_argument("--no_verify_certs", dest="verify_certs",
                        action="store_false",
                        help = "Do not verify ssl certificates")
    parser.set_defaults(verify_certs=True)

    args = parser.parse_args()
    return args

class Store():
    """Class to interact with a data source or sink.

    Stores can be either ElasticSearch indexes, or files. This class provides
    the means for reading from them, and writing to them.

    """

    def __init__(self):
        """Constructor for stores.

        Only some basic stuff at this root level.

        """

        self.still_items = True

    def _produce_item(self, item):
        """Produce an inem, based on the item read.

        The returned object should be a dictionary, ready for
        consumption.
        Default: just return item.

        """

        return item

    def read(self):
        """Read from the constructor, maybe using a buffer (generator).

        :return: Python generator returning items read from the data store.

        """

        read = 0
        for item in self.reader:
            read += 1
            if (read % 1000) == 0:
                print("Items read: {}".format(read),
                        end='\r')
            yield self._produce_item(item)
        print()

    def write(self, items):
        """Write an item to the constructor (maybe buffering).

        :param item: Item to write (generator)

        """

        pass

class ESStore(Store):
    """Class to interact with an ElasticSearch index.

    """

    def __init__(self, instance, index, create=False,
                verify_certs=True, match=None):
        """Constructor for ElasticSearch stores.

        In case there is a dictionary for matching, it will be
        of the form:
            {"match" : {
                field : value
                }}

        :param      str instance: url of the ElasticSearch instance
        :param         str index: index in ElasticSearch
        :param       bool create: create index or not
        :param bool verify_certs: don't verify SSL certificate
        :param             match: dictionary for matching

        """

        super().__init__()
        self.instance = instance
        self.index = index
        if match:
            self.query = {'query': match}
        else:
            self.query = None
        print("ElasticSearch: " + self.instance)
        try:
            self.es = elasticsearch.Elasticsearch(
                [self.instance],
                retry_on_timeout=True,
                verify_certs=verify_certs)
        except elasticsearch.exceptions.ImproperlyConfigured as exception:
            if exception.args[0].startswith("Root certificates are missing"):
                print("Error validating SSL certificate for {}.".format(self.instance))
                print("Use --no_verify_certs to avoid validation.")
                exit()
            else:
                raise
        if create:
            self.es.indices.create(self.index)
        scan_args = {'client': self.es, 'index': self.index}
        if self.query:
            scan_args['query'] = self.query
        self.reader = elasticsearch.helpers.scan(**scan_args)

    def _to_actions(self, items):
        """Generator which wraps items, preparing them as actions to be written.

        :param items: generator producing items to wrap

        """

        for item in items:
            to_write = {
                '_op_type': 'index',
                '_index': self.index,
                '_type': item['_type'],
                '_id': item['_id'],
                '_source': item['_source']
            }
            logging.debug("Actions: {}".format(to_write))
            yield to_write

    def write(self, items):
        """Write items to ElasticSearch instance and index.

        :param items: generator with items to write

        """

        actions = self._to_actions(items)
        elasticsearch.helpers.bulk(self.es, actions)

class FileStore(Store):
    """Class to interact with a file.

    """

    def __init__(self, path):
        """Constructor for file stores.

        :param      path: file path

        """

        super().__init__()
        self.path = path
        self.reader = open(self.path)
        print("File: " + self.path)

    def _produce_item(self, item):
        """Produce an inem, based on the item read.

        The returned object should be a dictionary, ready for
        consumption.
        Default: just return item.

        """

        return json.loads(item)

#    def read(self):
#        """Read from the constructor, maybe using a buffer (generator).

#        :return: Python genrator returning items read from the data store.

#        """

#        for item in open(self.path):
#            yield json.loads(item)

    def write(self, items):
        """Write items to ElasticSearch instance and index.

        :param items: generator with items to write

        """

        with open(self.path, 'w') as f:
            for item in items:
                f.write(json.dumps(item) + '\n')

def main():
    args = parse_args()
    if args.logging:
        log_format = '%(levelname)s:%(message)s'
        if args.logging == "info":
            level = logging.INFO
        elif args.logging == "debug":
            level = logging.DEBUG
        if args.logfile:
            logging.basicConfig(format=log_format, level=level,
                                filename = args.logfile, filemode = "w")
        else:
            logging.basicConfig(format=log_format, level=level)

    if args.src.startswith('http://') or args.src.startswith('https://'):
        if args.match:
            match = {"match" : {
                args.match[0] : args.match[1]
                }}
            print("Filtering for {}={}".format(args.match[0],
                                                args.match[1]))
        else:
            match = None
        src = ESStore(instance=args.src, index=args.src_index,
                        verify_certs=args.verify_certs,
                        match = match)
    else:
        src = FileStore(path=args.src)

    if args.dest.startswith('http://') or args.dest.startswith('https://'):
        dest = ESStore(instance=args.dest, index=args.dest_index,
                        verify_certs=args.verify_certs)
    else:
        dest = FileStore(path=args.dest)

    dest.write(src.read())

if __name__ == "__main__":
    main()
