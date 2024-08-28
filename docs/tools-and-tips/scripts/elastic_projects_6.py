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
from pprint import pprint
import urllib3

import elasticsearch
import elasticsearch.helpers

from xlrd import open_workbook

description = """Update 'project' field in a GrimoireLab index.

Reads data from an Excel spreadsheet

Example:
    elastic_projects --es http://elasctic.instance.xxx --index_git git \ --projects projects.xlsx --no_verify_certs --scroll_period 20m \ --max_chunk 100000

"""

# Disable warning about not verifying certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_args ():

    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("-l", "--logging", type=str, choices=["info", "debug"],
                        help = "Logging level for output")
    parser.add_argument("--logfile", type=str,
                            help = "Log file")
    parser.add_argument("--es", type=str, required=True,
                        help = "ElasticSearch url")
    parser.add_argument("--index_git", type=str,
                        help = "Git index to update")
    parser.add_argument("--index_github", type=str,
                        help = "GitHub index to update")
    parser.add_argument("--index_email", type=str,
                        help = "Email messages index to update")
    parser.add_argument("--projects", type=str,
                        help = "Excel file with projects data")
    parser.add_argument("--show_projects",
                        action="store_true",
                        help = "Show found projects")
    parser.add_argument("--verify_certs", dest="verify_certs",
                        action="store_true",
                        help = "Verify ssl certificates")
    parser.add_argument("--no_verify_certs", dest="verify_certs",
                        action="store_false",
                        help = "Do not verify ssl certificates")
    parser.add_argument("--scroll_period", default=u'5m',
                        help = "Period to maintain the scroll object in ES")
    parser.add_argument("--max_chunk", default=104857600, type=int,
                        help = "Max chunk size for data upload (default: 100MB)")
    parser.set_defaults(verify_certs=True)

    args = parser.parse_args()
    return args

class Index():
    """Class to interact with an ElasticSearch index.

    This class provides the means for reading from it, and writing to it.

    """

    def __init__(self, instance, change_op,
                scroll_period, max_chunk, verify_certs=True):
        """Constructor for ElasticSearch indexes.

        change_ops is a dictionary which encodes the change operation
        to perform on the index. It includes several fields:
          - index: the index name
          - to_check: the fields to check in the index
          - to_change: the fields to change in the index

        :param      str instance: url of the ElasticSearch instance
        :param    dict change_op: index in ElasticSearch
        :param scroll_period:     period for scroll object (eg: u'5m')
        :param max_chunk:         max chunk size for bulk upload (bytes)
        :param bool verify_certs: don't verify SSL certificate

        """

        self.still_items = True
        self.instance = instance
        self.index = change_op['index']
        self.to_check = change_op['to_check']
        self.to_change = change_op['to_change']
        # to_get are fields to retrieve from ElasticSearch
        self.to_get = self.to_check + self.to_change
        self.scroll_period = scroll_period
        self.max_chunk = max_chunk
        logging.debug("ElasticSearch instance: " + self.instance)
        try:
            self.es = elasticsearch.Elasticsearch([self.instance],
                                                verify_certs=verify_certs)
        except elasticsearch.exceptions.ImproperlyConfigured as exception:
            if exception.args[0].startswith("Root certificates are missing"):
                print("Error validating SSL certificate for {}.".format(self.instance))
                print("Use --no_verify_certs to avoid validation.")
                exit()
            else:
                raise
        # _source parameter to get only the fields we need
        self.reader = elasticsearch.helpers.scan(client=self.es,
                                index=self.index,
                                scroll=self.scroll_period,
                                _source=self.to_check+self.to_change)


    def read(self):
        """Read from the index, maybe using a buffer (generator).

        :return: Python genrator returning items read from the data store.

        """

        for item in self.reader:
            yield item

    def _normalize_values(self, values):
        """Normalize values obtained from the database, if needed.

        """

        return values

    def _get_from_item(self, item):
        """Get the relevant fields from an item in the index.

        :param item: item in the index
        :return:     list with relevant fields
        """

        values = []
        for field in self.to_get:
            values.append(item['_source'][field])
        values = self._normalize_values(values)
        return values

    def update(self, items):
        """Generator which updates project field in items.

        :param items: generator producing items to wrap

        """

        self.updated = 0
        self.retrieved = 0
        for item in items:
#            pprint(item)
            self.retrieved += 1
            (repo, project) = self._get_from_item(item)
            logging.info("Repo to update: " + repo)
            if repo in self.projects:
                project_new = self.projects[repo]
                logging.info("Project: " + project_new)
            else:
                project_new = 'Not tracked'
                logging.info("Repo not found in spreadsheet: " + repo)
            if project != project_new:
                to_write = {
                    '_op_type': 'update',
                    '_index': self.index,
                    '_type': item['_type'],
                    '_id': item['_id'],
                    'doc': {'project': project_new}
                    }
                if project_new in self.projects_found:
                    self.projects_found[project_new] += 1
                else:
                    self.projects_found[project_new] = 1
                logging.debug("Actions: {}".format(to_write))
                self.updated += 1
                yield to_write
            else:
                logging.info("Project already as it should: " + project)
            if (self.retrieved % 1000) == 0:
                print("Retrieved: {}, updated: {}".format(self.retrieved,
                                                            self.updated),
                        end='\r')
        print()

    def write(self, items, projects):
        """Write items to ElasticSearch instance and index.

        :param items:    generator with items to write
        :param projects: dictionary with the project for each repo
        """

        self.projects = projects
        self.projects_found = {}
        actions = self.update(items)
        elasticsearch.helpers.bulk(self.es, actions,
            max_chunk_bytes=self.max_chunk)
        for project in sorted(self.projects_found.keys()):
            print("Project:", project,
                    "repos: ", self.projects_found[project])
        print("Items retrieved:", self.retrieved)
        print("Items updated:", self.updated)

class Index_Git(Index):
    """Class for git commits.

    """

    def _normalize_values(self, values):
        """Normalize values obtained from the database.

        Normalize GitHub repo names, and remove the trailing '.git'

        """

        values[0] = normalized_ghrepo(values[0])[0:-4]
        return values

class Index_GitHub(Index):
    """Class for GitHub issues and pull requests.

    """

    def _normalize_values(self, values):
        """Normalize GitHub repo names.

        """

        values[0] = normalized_ghrepo(values[0])
        return values

class Index_Email(Index):
    """Class for email messages.

    """

    pass


class Sheet ():
    """Deal with sheets (generic code).

    First line: headers (usually, just ignore)

    """

    def __init__(self, sheet):
        """Constructor

        :param sheet: sheet in the spreadsheet

        """

        logging.debug("Sheet: " + sheet.name)
        # Name of the sheet
        self.sheet = sheet
        # Dictionary for repos (key is project, value number of
        # repos_projects)
        self.repos = {}
        # Dictionary for projects (key is repo, value is project)
        self.projects = {}

    def _normalize_repo(self, repo):
        """Normalize repository name.

        By default, nothing to do.

        """

        return repo

    def get_repos(self, show_projects=False):
        """Get dictionary with repos pointing to their projects.

        """

        # Read all rows with data in spreadsheet (skip header)
        for row in range(1,self.sheet.nrows):
            repo = self._normalize_repo(self.sheet.cell(row,0).value)
            project = self.sheet.cell(row,1).value
            logging.info("Found in spreadsheet: {}, {}".format(repo, project))
            if project == '':
                project = 'Unknown'
            self.projects[repo] = project
            if project in self.repos:
                self.repos[project] += 1
            else:
                self.repos[project] = 1
        if show_projects:
            print("Repos found in spreadsheet (per project)")
            for project in sorted(self.repos.keys()):
                print("Project:", project, "repos: ",
                    self.repos[project])
        return self.projects

def normalized_ghrepo(repo):
    """Repos come in several ways, they need to be normalized.

    'https://' is changed to 'http://'
    Uppercase is changed to lowercase

    :param repo: repo to normalized

    """

    normalized = repo.replace('https://','http://',1)
    normalized = normalized.lower()
    return normalized

class GitHubSheet (Sheet):
    """Deal with GitHub sheet.

    First column: GitHub repo (full url)
    Second column: project

    """

    def _normalize_repo(self, repo):

        return normalized_ghrepo(repo)

class EmailSheet (Sheet):
    """Deal with Email sheet.

    First column: Email list name
    Second column: project

    """

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

    if args.projects:
        wb = open_workbook('projects.xlsx')
        for sheet in wb.sheets():
            if (sheet.name == 'Github') and \
                (args.index_git or args.index_github):
                sheet_obj = GitHubSheet(sheet)
                repos_projects = sheet_obj.get_repos(
                        show_projects = args.show_projects)
            elif (sheet.name == "Mailing lists") and args.index_email:
                sheet_obj = EmailSheet(sheet)
                repos_projects = sheet_obj.get_repos(
                        show_projects = args.show_projects)

    # Change operations to perform (one per kind of index)
    change_ops = {}

    if args.index_git:
        change_ops['git'] = {'index': args.index_git,
            'to_check': ['repo_name'],
            'to_change': ['project']
            }
    if args.index_github:
        change_ops['github'] = {'index': args.index_github,
            'to_check': ['origin'],
            'to_change': ['project']
            }
    if args.index_email:
        change_ops['email'] = {'index': args.index_email,
            'to_check': ['list'],
            'to_change': ['project']
            }

    for change_op in change_ops:
        if change_op == 'git':
            index = Index_Git(instance=args.es,
                change_op=change_ops['git'],
                scroll_period= args.scroll_period,
                max_chunk=args.max_chunk,
                verify_certs=args.verify_certs)
        elif change_op == 'github':
            index = Index_GitHub(instance=args.es,
                change_op=change_ops['github'],
                scroll_period= args.scroll_period,
                max_chunk=args.max_chunk,
                verify_certs=args.verify_certs)
        elif change_op == 'email':
            index = Index_Email(instance=args.es,
                change_op=change_ops['email'],
                scroll_period= args.scroll_period,
                max_chunk=args.max_chunk,
                verify_certs=args.verify_certs)
        else:
            print("Change operation {} not implemented.".format(change_op))
            raise NotImplementedError
        index.write(index.read(), repos_projects)

if __name__ == "__main__":
    main()
