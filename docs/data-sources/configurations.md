---
layout: default
title: Configurations
nav_order: 2
parent: Data Sources
---

# Configurations

GrimoireLab supports a lot of data sources and the configurations to be ported
to `projects.json` and `setup.cfg` might differ per data source. You can find
the list of configurations according to each data source supported down below.

---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## askbot

Questions and answers from Askbot site

- projects.json

```
{
    "Chaoss": {
        "askbot": [
            "https://askbot.org/"
        ]
    }
}
```

- setup.cfg

```
[askbot]
raw_index = askbot_raw
enriched_index = askbot_enriched
```

## bugzilla

Bugs from Bugzilla

- projects.json

```
{
    "Chaoss": {
        "bugzilla": [
            "https://bugs.eclipse.org/bugs/"
        ]
    }
}
```

- setup.cfg

```
[bugzilla]
raw_index = bugzilla_raw
enriched_index = bugzilla_enriched
# The following setting is optional
backend-user = yyyy 
# The following setting is optional
backend-password = xxxx 
# The following setting is suggested
no-archive = true 
```

## bugzillarest

Bugs from Bugzilla server (>=5.0) using its REST API

- projects.json

```
{
    "Chaoss": {
        "bugzillarest": [
            "https://bugzilla.mozilla.org"
        ]
    }
}
```

- setup.cfg

```
[bugzillarest]
raw_index = bugzillarest_raw
enriched_index = bugzillarest_enriched
# The following setting is optional
backend-user = yyyy 
# The following setting is optional
backend-password = xxxx 
# The following setting is suggested
no-archive = true 
```

## cocom

Code complexity integration. Some graal dependencies like `cloc` might be
required,
https://github.com/chaoss/grimoirelab-graal#how-to-installcreate-the-executables

- projects.json

```
{
    "Chaoss":{
        "cocom": [
            "https://github.com/chaoss/grimoirelab-toolkit"
        ]
    }
}
```

- setup.cfg

```
[cocom]
raw_index = cocom_chaoss
enriched_index = cocom_chaoss_enrich
category = code_complexity_lizard_file
studies = [enrich_cocom_analysis]
branches = master
worktree-path = /tmp/cocom/
```

## colic

Code license backend.

- projects.json

```
{
    "Chaoss":{
        "colic": [
            "https://github.com/chaoss/grimoirelab-toolkit"
        ]
    }
}
```

- setup.cfg

```
[colic]
raw_index = colic_chaoss
enriched_index = colic_chaoss_enrich
category = code_license_nomos
studies = [enrich_colic_analysis]
exec-path = /usr/share/fossology/nomos/agent/nomossa
branches = master
worktree-path = /tmp/colic
```

## confluence

contents from Confluence

- projects.json

```
{
    "Chaoss": {
        "confluence": [
            "https://wiki.open-o.org/"
        ]
    }
}
```

- setup.cfg

```
[confluence]
raw_index = confluence_raw
enriched_index = confluence_enriched
# The following setting is suggested
no-archive = true 
```

## crates

packages from Crates.io

- projects.json

```
{
    "Chaoss": {
        "crates": [
            ""
        ]
    }
}
```

- setup.cfg

```
[crates]
raw_index = crates_raw
enriched_index = crates_enriched
```

## discourse

Topics from Discourse

- projects.json

```
{
    "Chaoss": {
        "discourse": [
            "https://foro.mozilla-hispano.org/"
        ]
    }
}
```

- setup.cfg

```
[discourse]
raw_index = discourse_raw
enriched_index = discourse_enriched
# The following setting is suggested
no-archive = true 
```

## dockerhub

Repositories info from DockerHub

- projects.json

```
{
    "Chaoss": {
        "dockerhub": [
            "bitergia kibiter"
        ]
    }
}
```

- setup.cfg

```
[dockerhub]
raw_index = dockerhub_raw
enriched_index = dockerhub_enriched
# The following setting is suggested
no-archive = true 
```

## dockerdeps

Dependencies extracted from Docker files. Requires
https://github.com/crossminer/crossJadolint

- projects.json

```
{
    "Chaoss": {
        "dockerdeps": [
            "https://github.com/chaoss/grimoirelab"
        ]
    }
}
```

- setup.cfg

```
[dockerdeps]
raw_index = dockerdeps_raw
enriched_index = dockerdeps_enrich
category = code_dependencies_jadolint
exec-path = <jadolint-local-path>/jadolint.jar
in-paths = [Dockerfile, Dockerfile-full, Dockerfile-secured, Dockerfile-factory, Dockerfile-installed]
```

## dockersmells

Smells extracted from Docker files. Requires
https://github.com/crossminer/crossJadolint

- projects.json

```
{
    "Chaoss": {
        "dockersmells": [
            "https://github.com/chaoss/grimoirelab"
        ]
    }
}
```

- setup.cfg

```
[dockersmells]
raw_index = dockersmells_raw
enriched_index = dockersmells_enrich
category = code_quality_jadolint
exec-path = <jadolint-local-path>/jadolint.jar
in-paths = [Dockerfile, Dockerfile-full, Dockerfile-secured, Dockerfile-factory, Dockerfile-installed]
```

## functest

Tests from functest

- projects.json

```
{
    "Chaoss": {
        "functest": [
            "http://testresults.opnfv.org/test/"
        ]
    }
}
```

- setup.cfg

```
[functest]
raw_index = functest_raw
enriched_index = functest_enriched
# The following setting is suggested
no-archive = true 
```

## gerrit

Reviews from Gerrit

You have to add your public key in the gerrit server.

- projects.json

```
{
    "Chaoss": {
        "gerrit": [
            "review.opendev.org"
        ]
    }
}
```

- setup.cfg

```
[gerrit]
raw_index = gerrit_raw
enriched_index = gerrit_enriched
user = xxxx
# The following section is suggested
no-archive = true 
# The following section is optional
blacklist-ids = [] 
# The following section is optional
max-reviews = 500 
# The following section is optional
studies = [enrich_demography:gerrit, enrich_onion:gerrit, enrich_demography_contribution:gerrit] 

# The following section is optional
[enrich_demography:gerrit] 

# The following section is optional
[enrich_onion:gerrit] 
in_index = gerrit_enriched
out_index = gerrit-onion_enriched

# The following section is optional
[enrich_demography_contribution:gerrit] 
date_field = grimoire_creation_date
author_field = author_uuid
```

## git

Commits from Git

**Note:** If you want to analyze private git repositories, make sure you pass the credentials directly in the URL.

- projects.json

```
{
    "Chaoss": {
        "git": [
            "https://github.com/chaoss/grimoirelab-perceval",
            "https://<username>:<api-token>@github.com/chaoss/grimoirelab-sirmordred"
        ]
    }
}
```

- setup.cfg

```
[git]
raw_index = git_raw
enriched_index = git_enriched
# The following setting is suggested
latest-items = true 
# The following setting is optional
studies = [enrich_demography:git, enrich_git_branches:git, enrich_areas_of_code:git, enrich_onion:git, enrich_extra_data:git] 

# The following section is optional
[enrich_demography:git] 

# The following section is optional
[enrich_git_branches:git] 
# The following setting is optional
run_month_days = [1, 23] 

# The following section is optional
[enrich_areas_of_code:git] 
in_index = git_raw
out_index = git-aoc_enriched

# The following section is optional
[enrich_onion:git] 
in_index = git_enriched
out_index = git-onion_enriched

[enrich_extra_data:git]
json_url = https://gist.githubusercontent.com/zhquan/bb48654bed8a835ab2ba9a149230b11a/raw/5eef38de508e0a99fa9772db8aef114042e82e47/bitergia-example.txt

[enrich_forecast_activity]
out_index = git_study_forecast
```

## github

Issues and PRs from GitHub

### issue

- projects.json

```
{
    "Chaoss": {
        "github:issue": [
            "https://github.com/chaoss/grimoirelab-perceval",
            "https://github.com/chaoss/grimoirelab-sirmordred"
        ]
    }
}
```

- setup.cfg

```
[github:issue]
raw_index = github_raw
enriched_index = github_enriched
api-token = xxxx
category = issue
sleep-for-rate = true
# The following setting is suggested
no-archive = true 
studies = [enrich_onion:github,
           enrich_geolocation:user,
           enrich_geolocation:assignee,
           enrich_extra_data:github,
           enrich_backlog_analysis,
           # The following setting is optional
           enrich_demography:github] 

# The following section is optional
[enrich_onion:github] 
in_index_iss = github_issues_onion-src
in_index_prs = github_prs_onion-src
out_index_iss = github-issues-onion_enriched
out_index_prs = github-prs-onion_enriched

# The following section is optional
[enrich_geolocation:user] 
location_field = user_location
geolocation_field = user_geolocation

# The following section is optional
[enrich_geolocation:assignee] 
location_field = assignee_location
geolocation_field = assignee_geolocation

[enrich_extra_data:github]
json_url = https://gist.githubusercontent.com/zhquan/bb48654bed8a835ab2ba9a149230b11a/raw/5eef38de508e0a99fa9772db8aef114042e82e47/bitergia-example.txt

[enrich_backlog_analysis]
out_index = github_enrich_backlog
interval_days = 7
reduced_labels = [bug,enhancement]
map_label = [others, bugs, enhancements]

[enrich_demography:github]
```

### pull request

- projects.json

```
{
    "Chaoss": {
        "github:pull": [
            "https://github.com/chaoss/grimoirelab-perceval",
            "https://github.com/chaoss/grimoirelab-sirmordred"
        ]
    }
}
```

- setup.cfg

```
[github:pull]
raw_index = github-pull_raw
enriched_index = github-pull_enriched
api-token = xxxx
category = pull_request
sleep-for-rate = true
# The following setting is suggested
no-archive = true 
studies = [enrich_geolocation:user,
           enrich_geolocation:assignee,
           enrich_extra_data:github,
           # The following setting is optional
           enrich_demography:github] 

[enrich_geolocation:user]
location_field = user_location
geolocation_field = user_geolocation

[enrich_geolocation:assignee]
location_field = assignee_location
geolocation_field = assignee_geolocation

[enrich_extra_data:github]
json_url = https://gist.githubusercontent.com/zhquan/bb48654bed8a835ab2ba9a149230b11a/raw/5eef38de508e0a99fa9772db8aef114042e82e47/bitergia-example.txt

[enrich_demography:github]
```

### repo

The number of forks, starts, and subscribers in the repository.

- projects.json

```
{
    "Chaoss": {
        "github:repo": [
            "https://github.com/chaoss/grimoirelab-perceval",
            "https://github.com/chaoss/grimoirelab-sirmordred"
        ]
    }
}
```

- setup.cfg

```
[github:repo]
raw_index = github-repo_raw
enriched_index = github-repo_enriched
api-token = xxxx
category = repository
sleep-for-rate = true
# The following setting is suggested
no-archive = true 
studies = [enrich_extra_data:github, enrich_demography:github]

[enrich_extra_data:github]
json_url = https://gist.githubusercontent.com/zhquan/bb48654bed8a835ab2ba9a149230b11a/raw/5eef38de508e0a99fa9772db8aef114042e82e47/bitergia-example.txt

[enrich_demography:github]
```

## githubql

Events from GitHub

The corresponding dashboards can be automatically uploaded by setting
`github-events` to `true` in the `panels` section within the `setup.cfg`

- projects.json

```
{
    "Chaoss": {
        "githubql": [
            "https://github.com/chaoss/grimoirelab-toolkit"
        ]
    }
}
```

- setup.cfg

```
[panels]
github-events = true

[githubql]
raw_index = github_event_raw
enriched_index = github_event_enriched
api-token = xxxxx
sleep-for-rate = true
# The following setting is optional
sleep-time = "300" 
# The following setting is suggested
no-archive = true 
# The following setting is optional
studies = [enrich_duration_analysis:kanban, enrich_reference_analysis] 

[enrich_duration_analysis:kanban]
start_event_type = MovedColumnsInProjectEvent
fltr_attr = board_name
target_attr = board_column
fltr_event_types = [MovedColumnsInProjectEvent, AddedToProjectEvent]

[enrich_duration_analysis:label]
start_event_type = UnlabeledEvent
target_attr = label
fltr_attr = label
fltr_event_types = [LabeledEvent]

# The following section is optional
[enrich_reference_analysis] 
```

## github2

Comments from GitHub

The corresponding dashboards can be automatically uploaded by setting
`github-comments` to `true` in the `panels` section within the `setup.cfg`

### issue

- projects.json

```
{
    "Chaoss": {
        "github2:issue": [
            "https://github.com/chaoss/grimoirelab-perceval",
            "https://github.com/chaoss/grimoirelab-sirmordred"
        ]
    }
}
```

- setup.cfg

```
[github2:issue]
api-token = xxxx
raw_index = github2-issues_raw
enriched_index = github2-issues_enriched
sleep-for-rate = true
category = issue
# The following setting is suggested
no-archive = true 
# The following setting is optional
studies = [enrich_geolocation:user, enrich_geolocation:assignee, enrich_extra_data:github2, enrich_feelings] 

# The following section is optional
[enrich_geolocation:user] 
location_field = user_location
geolocation_field = user_geolocation

# The following section is optional
[enrich_geolocation:assignee] 
location_field = assignee_location
geolocation_field = assignee_geolocation

[enrich_extra_data:github2]
json_url = https://gist.githubusercontent.com/zhquan/bb48654bed8a835ab2ba9a149230b11a/raw/5eef38de508e0a99fa9772db8aef114042e82e47/bitergia-example.txt

[enrich_feelings]
attributes = [title, body]
nlp_rest_url = http://localhost:2901
```

### pull request

- projects.json

```
{
    "Chaoss": {
        "github2:pull": [
            "https://github.com/chaoss/grimoirelab-perceval",
            "https://github.com/chaoss/grimoirelab-sirmordred"
        ]
    }
}
```

- setup.cfg

```
[github2:pull]
api-token = xxxx
raw_index = github2-pull_raw
enriched_index = github2-pull_enriched
sleep-for-rate = true
category = pull_request
# The following setting is suggested
no-archive = true 
# The following setting is optional
studies = [enrich_geolocation:user, enrich_geolocation:assignee, enrich_extra_data:git, enrich_feelings] 

# The following section is optional
[enrich_geolocation:user] 
location_field = user_location
geolocation_field = user_geolocation

# The following section is optional
[enrich_geolocation:assignee] 
location_field = assignee_location
geolocation_field = assignee_geolocation

[enrich_extra_data:github2]
json_url = https://gist.githubusercontent.com/zhquan/bb48654bed8a835ab2ba9a149230b11a/raw/5eef38de508e0a99fa9772db8aef114042e82e47/bitergia-example.txt

[enrich_feelings]
attributes = [title, body]
nlp_rest_url = http://localhost:2901
```

## gitlab

Issues and MRs from GitLab

GitLab issues and merge requests need to be configured in two different
sections. The corresponding dashboards can be automatically uploaded by setting
`gitlab-issue` and `gitlab-merge` to `true` in the `panels` section within the
`setup.cfg`

If a given GitLab repository is under more than 1 level, all the slashes `/`
starting from the second level have to be replaced by `%2F`. For instance, for a
repository with a structure similar to this one
`https://gitlab.com/Molly/lab/first`.

### issue

- projects.json

```
{
    "Chaoss": {
        "gitlab:issue": [
            "https://gitlab.com/Molly/first",
            "https://gitlab.com/Molly/lab%2Fsecond"
        ]
    }
}
```

- setup.cfg

```
[panels]
gitlab-issues = true

[gitlab:issue]
category = issue
raw_index = gitlab-issues_raw
enriched_index = gitlab-issues_enriched
api-token = xxxx
sleep-for-rate = true
# The following setting is suggested
no-archive = true 
# The following setting is optional
studies = [enrich_onion:gitlab-issue] 

# The following section is optional
[enrich_onion:gitlab-issue] 
in_index = gitlab-issues_enriched
out_index = gitlab-issues-onion_enriched
data_source = gitlab-issues
```

### merge request

- projects.json

```
{
    "Chaoss": {
        "gitlab:merge": [
            "https://gitlab.com/Molly/first",
            "https://gitlab.com/Molly/lab%2Fsecond"
        ],
    }
}
```

- setup.cfg

```
[panels]
gitlab-merges = true

[gitlab:merge]
category = merge_request
raw_index = gitlab-mrs_raw
enriched_index = gitlab-mrs_enriched
api-token = xxxx
sleep-for-rate = true
# The following setting is suggested
no-archive = true 
# The following setting is optional
studies = [enrich_onion:gitlab-merge] 

# The following section is optional
[enrich_onion:gitlab-merge] 
in_index = gitlab-mrs_enriched
out_index = gitlab-mrs-onion_enriched
data_source = gitlab-merges

```

## gitter

Messages from gitter rooms

- projects.json

```
{
    "Chaoss": {
        "gitter": [
            "https://gitter.im/jenkinsci/jenkins",
        ]
    }
}
```

- setup.cfg

```
[gitter]
raw_index = gitter_raw
enriched_index = gitter_enriched_raw
api-token = xxxxx
sleep-for-rate = true
# The following setting is optional
sleep-time = "300" 
# The following setting is suggested
no-archive = true 
```

## google_hits

Number of hits for a set of keywords from Google

- projects.json

```
{
    "Chaoss": {
        "google_hits": [
            "bitergia grimoirelab"
        ]
    }
}
```

- setup.cfg

```
[google_hits]
raw_index = google_hits_raw
enriched_index =google_hits_enriched
```

## groupsio

Messages from Groupsio

To know the lists you are subscribed to:
https://gist.github.com/valeriocos/ad33a0b9b2d13a8336230c8c59df3c55

- projects.json

```
{
    "Chaoss": {
        "groupsio": [
            "group1",
            "group2"
        ]
    }
}
```

- setup.cfg

```
[groupsio]
raw_index = groupsio_raw
enriched_index = groupsio_enriched
email = yyyy
password = xxxx
```

## hyperkitty

Messages from a HyperKitty

- projects.json

```
{
    "Chaoss": {
        "hyperkitty": [
            "https://lists.mailman3.org/archives/list/mailman-users@mailman3.org"
        ]
    }
}
```

- setup.cfg

```
[hyperkitty]
raw_index = hyperkitty_raw
enriched_index = hyperkitty_enriched
```

## jenkins

Builds from a Jenkins

- projects.json

```
{
    "Chaoss": {
        "jenkins": [
            "https://build.opnfv.org/ci"
        ]
    }
}
```

- setup.cfg

```
[jenkins]
raw_index = jenkins_raw
enriched_index = jenkins_enriched
# The following setting is suggested
no-archive = true 
```

## jira

Issues data from JIRA issue trackers

- projects.json

```
{
    "Chaoss":{
        "jira": [
            "https://jira.opnfv.org"
        ]
    }
}
```

- setup.cfg

```
[jira]
raw_index = jira_raw
enriched_index = jira_enriched
# The following setting is optional
project = JIRAPROJECT 
# The following setting is suggested
no-archive = true 
# The following setting is optional
backend-user = yyyy 
# The following setting is optional
backend-password = xxxx 
```

## kitsune

Questions and answers from KitSune

- projects.json

```
{
    "Chaoss": {
        "kitsune": [
            ""
        ]
    }
}
```

- setup.cfg

```
[kitsune]
raw_index = kitsune_raw
enriched_index = kitsune_enriched
```

## mattermost

Messages from Mattermost channels

- projects.json

```
{
    "Chaoss": {
        "mattermost": [
            "https://chat.openshift.io 8j366ft5affy3p36987pcugaoa"
        ]
    }
}
```

- setup.cfg

```
[mattermost]
raw_index = mattermost_raw
enriched_index = mattermost_enriched
api-token = xxxx
```

## mbox

Messages from MBox files

For mbox files, it is needed the name of the mailing list and the path where the
mboxes can be found. In the example below, the name of the mailing list is set
to "mirageos-devel".

- projects.json

```
{
    "Chaoss": {
        "mbox": [
            "mirageos-devel /home/bitergia/mbox/mirageos-devel/"
        ]
    }
}
```

- setup.cfg

```
[mbox]
raw_index = mbox_raw
enriched_index = mbox_enriched
```

## mediawiki

Pages and revisions from MediaWiki

-projects.json

```
{
    "Chaoss": {
        "mediawiki": [
            "https://www.mediawiki.org/w https://www.mediawiki.org/wiki"
        ]
    }
}
```

- setup.cfg

```
[mediawiki]
raw_index = mediawiki_raw
enriched_index = mediawiki_enriched
# The following setting is suggested
no-archive = true 
```

## meetup

Events from Meetup groups

For meetup groups it is only needed the identifier of the meetup group and an
API token:
https://chaoss.github.io/grimoirelab-tutorial/gelk/meetup.html#gathering-meetup-groups-data

- projects.json

```
{
    "Chaoss": {
        "meetup": [
        "Alicante-Bitergia-Users-Group",
        "South-East-Bitergia-User-Group"
        ]
    }
}
```

- setup.cfg

```
[meetup]
raw_index = meetup_raw
enriched_index = meetup_enriched
api-token = xxxx
sleep-for-rate = true
# The following setting is optional
sleep-time = "300" 
# The following setting is suggested
no-archive = true 

```

## mozillaclub

Events from Mozillaclub

- projects.json

```
{
    "Chaoss": {
        "mozillaclub": [
            "https://spreadsheets.google.com/feeds/cells/1QHl2bjBhMslyFzR5XXPzMLdzzx7oeSKTbgR5PM8qp64/ohaibtm/public/values?alt=json"
        ]
    }
}
```

- setup.cfg

```
[mozillaclub]
raw_index = mozillaclub_raw
enriched_index = mozillaclub_enriched
```

## nntp

Articles from NNTP newsgroups

The way to setup netnews is adding the server and the news channel to be
monitored. In the example below, the `news.myproject.org` is the server name.

- projects.json

```
{
    "Chaoss": {
        "nntp": [
            "news.myproject.org mozilla.dev.tech.crypto.checkins",
            "news.myproject.org mozilla.dev.tech.electrolysis",
            "news.myproject.org mozilla.dev.tech.gfx",
            "news.myproject.org mozilla.dev.tech.java"
        ]
    }
}
```

- setup.cfg

```
[nntp]
raw_index = nntp_raw
enriched_index =  nntp_enriched
```

## pagure

Issues from Pagure repositories

- projects.json

```
{
    "Chaoss": {
        "pagure": [
            "https://pagure.io/Test-group/Project-example-namespace"
        ]
    }
}
```

- setup.cfg

```
[pagure]
raw_index = pagure_raw
enriched_index = pagure_enriched
api-token = xxxx
sleep-for-rate = true
# The following setting is optional
sleep-time = "300" 
# The following setting is suggested
no-archive = true 
```

## phabricator

Tasks from Phabricator

- projects.json

```
{
    "Chaoss": {
        "phabricator": [
            "https://phabricator.wikimedia.org"
        ]
    }
}
```

- setup.cfg

```
[phabricator]
raw_index = phabricator_raw
enriched_index = phabricator_enriched
api-token = xxxx
# The following setting is suggested
no-archive = true 
```

## pipermail

Messages from Pipermail

- projects.json

```
{
    "Chaoss": {
        "pipermail": [
            "https://lists.linuxfoundation.org/pipermail/grimoirelab-discussions/"
        ]
    }
}
```

- setup.cfg

```
[pipermail]
raw_index = pipermail_raw
enriched_index = pipermail_enriched
```

## puppetforge

Modules and their releases from Puppet's forge

- projects.json

```
{
    "Chaoss": {
        "puppetforge": [
            ""
        ]
    }
}
```

- setup.cfg

```
[puppetforge]
raw_index = puppetforge_raw
enriched_index = puppetforge_enriched
```

## redmine

Issues from Redmine

- project.json

```
{
    "Chaoss": {
        "redmine": [
            "http://tracker.ceph.com/"
        ]
    }
}
```

- setup.cfg

```
[redmine]
raw_index = redmine_raw
enriched_index = redmine_enriched
api-token = XXXXX
```

## remo

Events, people and activities from ReMo

- project.json

```
{
    "Chaoss": {
        "remo": [
            "https://reps.mozilla.org"
        ]
    }
}
```

- setup.cfg

```
[remo]
raw_index = remo_raw
enriched_index = remo_enriched
```

## rocketchat

Messages from Rocketchat channels

- projects.json

```
{
    "Chaoss": {
        "rocketchat": [
            "https://open.rocket.chat general"
        ]
    }
}
```

- setup.cfg

```
[rocketchat]
raw_index = rocketchat_raw
enriched_index = rocketchat_enriched
api-token = xxxx
sleep-for-rate = true
user-id = xxxx
# The following setting is suggested
no-archive = true 
```

## rss

Entries from RSS feeds

- project.json

```
{
    "Chaoss": {
        "remo": [
            "https://reps.mozilla.org"
        ]
    }
}
```

- setup.cfg

```
[rss]
raw_index = rss_raw
enriched_index = rss_enriched
```

## slack

Messages from Slack channels

The information needed to monitor slack channels is the channel id.

- projects.json

```
{
    "Chaoss": {
        "slack": [
            "A195YQBLL",
            "A495YQBM2"
        ]
    }
}
```

- setup.cfg

```
[slack]
raw_index = slack_raw
enriched_index = slack_enriched
api-token = xxxx
# The following setting is suggested
no-archive = true 
```

## stackexchange

Questions, answers and comments from StackExchange

- projects.json

```
{
    "Chaoss": {
        "stackexchange": [
            "http://stackoverflow.com/questions/tagged/chef",
            "http://stackoverflow.com/questions/tagged/chefcookbook",
            "http://stackoverflow.com/questions/tagged/ohai",
            "http://stackoverflow.com/questions/tagged/test-kitchen",
            "http://stackoverflow.com/questions/tagged/knife"
        ]
    }
}
```

- setup.cfg

```
[stackexchange]
raw_index = stackexchange_raw
enriched_index = stackexchange_enriched
api-token = xxxx
# The following setting is suggested
no-archive = true 
```

## supybot

Messages from Supybot log files

For supybot files, it is needed the name of the IRC channel and the path where
the logs can be found. In the example below, the name of the channel is set to
"irc://irc.freenode.net/atomic".

- projects.json

```
{
    "Chaoss": {
        "supybot": [
            "irc://irc.freenode.net/atomic /home/bitergia/irc/percevalbot/logs/ChannelLogger/freenode/#atomic"
        ]
    }
}
```

- setup.cfg

```
[supybot]
raw_index = supybot_raw
enriched_index = supybot_enriched
```

## telegram

Messages from Telegram

You need to have an API token:
https://github.com/chaoss/grimoirelab-perceval#telegram

- projects.json

```
{
    "Chaoss": {
        "telegram": [
            "Mozilla_analytics"
        ]
    }
}
```

- setup.cfg

```
[telegram]
raw_index = telegram_raw
enriched_index = telegram_enriched
api-token = XXXXX
```

## twitter

Messages from Twitter

You need to provide a [search
query](https://developer.twitter.com/en/docs/tweets/search/guides/build-standard-query)
and an API token (which requires to create an
[app](https://developer.twitter.com/en/docs/basics/apps/overview)). The script
at https://gist.github.com/valeriocos/7d4d28f72f53fbce49f1512ba77ef5f6 helps
obtaining a token.

- projects.json

```
{
    "Chaoss": {
        "twitter": [
            "bitergia"
        ]
    }
}
```

- setup.cfg

```
[twitter]
raw_index = twitter_raw
enriched_index = twitter_enriched
api-token = XXXX
```

## weblate

Changes from Weblate

You need to have an API token: The token can be obtained after registering to a
weblate instance (e.g., https://translations.documentfoundation.org/), via the
page <instance>/accounts/profile/#api

- projects.json

```
{
    "Chaoss": {
        "weblate": [
            "https://translations.documentfoundation.org"
        ]
    }
}
```

- setup.cfg

```
[weblate]
raw_index = weblate_raw
enriched_index = weblate_enriched
api-token = XXXX
# The following setting is suggested
no-archive = true 
# The following setting is suggested
sleep-for-rate = true 
# The following setting is optional
studies = [enrich_demography:weblate] 

# The following section is optional
[enrich_demography:weblate] 
```
