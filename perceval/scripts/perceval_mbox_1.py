#! /usr/bin/env python3

import perceval.backends

# uri (label) for the mailing list to analyze
mbox_uri = 'http://mail-archives.apache.org/mod_mbox/httpd-announce/'
# directory for letting Perceval where mbox archives are
# you need to have the archives to analyzed there before running the script
mbox_dir = 'archives'

# create a mbox object, using mbox_uri as label, mbox_dir as directory to scan
repo = perceval.backends.mbox.MBox(uri=mbox_uri, dirpath=mbox_dir)
# fetch all messages as an iteratoir, and iterate it printing each subject
for commit in repo.fetch():
    print(commit['data']['Subject'])
