#! /usr/bin/env python3

import perceval.backends

# url for the git repo to analyze
repo_url = 'http://github.com/grimmoirelab/perceval.git'
# directory for letting Perceval clone the git repo
repo_dir = '/tmp/perceval.git'

# create a Git object, pointing to repo_url, using repo_dir for cloning
repo = perceval.backends.git.Git(uri=repo_url, gitpath=repo_dir)
# fetch all commits as an iteratoir, and iterate it printing each hash
for commit in repo.fetch():
    print(commit['data']['commit'])
