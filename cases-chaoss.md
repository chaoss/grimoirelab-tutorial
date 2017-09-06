# Cases: CHAOS Health Model

The [CHAOSS Metrics Technical Committee](https://wiki.linuxfoundation.org/oss-health-metrics) is working on defining metrics for assessing open source communities' health and sustainability. In this chapter we use some of their definitions, as of September 2017, to produce visualizations based on the GrimoireLab stack. They will be used to compose a "CHAOSS Metrics Dashboard" produced with GrimoireLab technology.

## Data collection

Before producing the visualizations, we need to grab the data and produce the corresponding raw indexes. Fortunately, most of the metrics the CHAOSS Metrics Committee is defining can be produced directly from GrimoireLab enriched indexes, so we will also produce enriched indexes.

As data sources, we will use the main repositories the [GitHub GrimoireLab organization](https://github.com/grimoirelab): Perceval, Arthur, GrimoireELK, SortingHat, Panels, Mordred, and Training. It would be easy to use any other collection of repositories, and the result will be illustrative enough.

The process shown here is completely manual, to minimize configuration and understanding of GrimoireLab components. It could be further automated with the use of Mordred and Arthur, specially if the data is to be updated continuously, but for now we will skip that part. In a first try we won't use SortingHat for simplicity: we can do that later, making some of the metrics more accurate.

The process will include the installation of the GrimoireLab tools needed, and will assume that Python3, MySQL/MariaDB, ElasticSearch and Kibana are already installed (see [Installation section](/grimoireelk/installation.md) for some hints on all of this.

Let's start by installing GrimoireLab components:

```bash
$ python3 -m venv gl
$ source gl/bin/activate
(gl) $ pip install grimoire-elk grimoire-kidash
```

Now, let's retrieve data for all the repositories to analyze (assuming ElasticSearch is local, available in its default port). We will use the following Python script, which will just run `p2o.py` for each repository to retrieve:

```python
#! !/usr/bin/env python3
# -*- coding: utf-8 -*-
# retrieve.py

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
```

To run it, we need to specify a [personal GitHub token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) in the command line. That token will be provided to the GitHub API to speed things a bit. Be careful with your token, and don't include it in anything which may became public (your personal token allows for access to GitHub with your permissions).

```
(gl) $ python3 retrieve.py <github_token>
```

After some minutes and a lot of messages, all the repositories will be retrieved, and the indexes will be produced. Now we can proceed to produce the metrics panels...