#! !/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
from sys import argv

token = argv[1]
repos = ['perceval', 'arthur', 'grimoireelk', 'sortinghat', 'mordred',
  'panels', 'training']

for repo in repos:
    # Produce git and git_raw indexes from git repo
    subprocess.run(['p2o.py', '--enrich', '--index', 'git_raw',
      '--index-enrich', 'git', '-e', 'http://localhost:9200',
      '--no_inc', '--debug', 'git',
      'https://github.com/grimoirelab/' + repo])
    # Produce github and github_raw indexes from GitHub issues and prs
    subprocess.run(['p2o.py', '--enrich', '--index', 'github_raw',
      '--index-enrich', 'github', '-e', 'http://localhost:9200',
      '--no_inc', '--debug', 'github', 'grimoirelab', repo,
      '-t', token, '--sleep-for-rate'])
