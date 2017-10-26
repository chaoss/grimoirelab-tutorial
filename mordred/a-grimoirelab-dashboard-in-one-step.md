## A GrimoireLab dashboard in one step

Mordred can produce a dashboard for a group of repositories in one step. It can produce the dashboard for many different data sources, and can do that icrementally (that is, periodically visiting all repositories, and updating the dashboard with new data). But to start small and easy, in this first example we will produce a dashobard for only two git repositories.

The process is as follows:

* Prepare a configuration file for Mordred. We're calling it, in this case, [mordred-grimoirelab.cfg](files/mordred-grimoirelab.cfg):

```
[general]
short_name = GrimoireLab
update = false
# in seconds
sleep = 0
min_update_delay = 10
debug = true
# /var/log/mordred/
logs_dir = /tmp/logs
kibana = "5"

[projects]
projects_file = projects.json

[es_collection]
url = http://localhost:9200
user =
password =

[es_enrichment]
url = http://127.0.0.1:9200
user =
password =

# Refresh identities and projects for all items after enrichment
autorefresh = false
studies = true

[sortinghat]
host = localhost
user = jgb
password = XXX
database = grimoirelab_sh
load_orgs = false
#orgs_file = /home/bitergia/conf/orgs_file
# see: sortinghat unify --help
unify_method =
# commonly: Unknown
unaffiliated_group = Unknown
affiliate = True
autoprofile = [customer,git,github]
matching = [email]
sleep_for = 0
bots_names = [Beloved Bot]

[panels]
kibiter_time_from= "now-90d"
kibiter_default_index= "git"

[phases]
collection = true
identities = true
enrichment = true
panels = true


[git]
raw_index = git_test-raw
enriched_index = git_test
```

* Prepare a [projects.json](files/projects.json) file, with the list of repositories to analyze, organized in projects. A very small version of it, just for testing:

```
{
    "grimoire": {
        "git": [
            "https://github.com/grimoirelab/perceval",
            "https://github.com/grimoirelab/grimoireelk"
        ]
    }
}
```

* Prepare a [menu.yaml](files/menu.yaml), with the menu for Kibiter (not needed if the data will be visualized with Kibana).

* Clone the [grimoirelab/panels](https://github.com/grimoirelab/panels) git repository, which has some pre-configured dashboards for Kibitter:

```
$ git clone https://github.com/grimoirelab/panels
```

* Run Mordred, in an enviroment with the appropriate programs installed: git, MariaDB (or MySQL), ElasticSearch, and Kibitter. The cloned `panels` repository should be a subdirectory, named `panels`, of the directory where the `mordred` command is run:

```
mordred -c mordred-grimoirelab.cfg
```

And that's it. Point your browser to [http://localhost:5601](http://localhost:5601), assuming your Kibiter is deployed to serve requests in the standard port (5601). You'll see the produced dashboard.