## A GrimoireLab dashboard in one step

[SirMordred](https://github.com/chaoss/grimoirelab-sirmordred)
is the GrimoireLab module in charge of orchestrating all
the processes leading to produce a dashboard or a report.
It runs Perceval, GrimoireELK, SortingHat, etc. to retrieve
data from the data sources, 
produce raw and enriched indexes in ElasticSearch,
load predefined visualizations and panels to the dashboard,
and all the stuff.

SirMordred can produce a dashboard for a group of repositories in one step,
for many different data sources, and can do that incrementally
(that is, periodically visiting all repositories,
and updating the dashboard with new data).
But to start small and easy, in this first example we will produce a dashboard
for only two git repositories.

The process is as follows:

* Prepare a configuration file for Mordred.
We're calling it, in this case, [mordred-simple.cfg](files/mordred-simple.cfg):

```
# Simple SirMordred config file
#

[general]
# Name of the project to analyze (will appear in dashboard)
short_name = TestProject
# Update incrementally, forever
update = true
# Don't start a new update earlier than (since last update, seconds)
min_update_delay = 50
# Produce debugging data for the logs
debug = true

# Directory for logs
logs_dir = logs


[projects]
# File with repositories to analyze
projects_file = projects.json


[es_collection]
# Url to access raw indexes (Elasticsearch instance)
url = http://localhost:9200
# User and password to acces Elasticseach, if any
user =
password =


[es_enrichment]
# Url to access enriched indexes (Elasticsearch instance)
url = http://127.0.0.1:9200
# User and password to acces Elasticseach, if any
user =
password =

# Refresh identities and projects for all items after enrichment
autorefresh = true


[sortinghat]
# Host to access MariaDB / MySQL instance
host = localhost
# User and password to access MariaDB / MySQL instance
user = mariadb_user
password = XXX
# Name of MariaDB / MySQL database
database = grimoirelab_sh

# Run affilation
affiliate = True
# How to match to unify
matching = [email]
# How long to sleep before running again, for identities tasks
sleep_for = 10
# Don't load a specific organizations file
load_orgs = false
# Name of group of identities with no affiliation
unaffiliated_group = Unknown
# Ids known to be bots
bots_names = [Beloved Bot]
# How to autoprofile
autoprofile = [TestProject:manual,git,github]

[panels]
# Kibitter / kibana entry point
kibiter_url = http://localhost:5601
# Dashboard: default time frame
kibiter_time_from= "now-1y"
# Dashboard: default index pattern
kibiter_default_index= "git"

[phases]
# Data collection (build raw indexes)
collection = true
# Run SortingHat for identities
identities = true
# Build enriched indexes
enrichment = true
# Upload panels to Kibiter/Kibana
panels = true

[git]
# Names for raw and enriched indexes
raw_index = git_grimoirelab-raw
enriched_index = git_grimoirelab
```

In this file, you need to include the proper credentials where needed. At least, you should change `user_sh` and `pass_sh` to your credentials to the SortingHat (MariaDB or MySQL) database.

* Prepare a [projects.json](files/projects.json) file, with the list of repositories to analyze, organized in projects. A very small version of it, just for testing:

```
{
    "Test Project": {
        "git": [
            "https://github.com/chaoss/grimoirelab-perceval",
            "https://github.com/chaoss/grimoirelab-elk"
        ]
    }
}
```

See a more complete information about this file in the [section on the projects file](projects.md).

* Prepare a [menu.yaml](files/menu.yaml), with the menu for Kibiter (not needed if the data will be visualized with Kibana).

* Run SirMordred, in an environment with the appropriate programs
installed: git, MariaDB (or MySQL), ElasticSearch, and Kibitter.

```
sirmordred -c mordred-simple.cfg
```

And that's it.
Point your browser to [http://localhost:5601](http://localhost:5601),
assuming your Kibiter is deployed to serve requests in the standard port (5601). You'll see the produced dashboard.
