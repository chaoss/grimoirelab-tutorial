#! /usr/bin/env python3
from graal.backends.core.cocom import CoCom

# URL for the git repo to analyze
repo_uri = "http://github.com/chaoss/grimoirelab-graal"

# directory where to mirror the repo
repo_dir = "/tmp/graal-cocom"

# Cocom object initialization
cc = CoCom(uri=repo_uri, git_path=repo_dir)

# fetch all commits
commits = [commit for commit in cc.fetch()]
