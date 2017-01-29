## Setting up the environment

To set up the complete environment to produce a Kibana-based dashboard based on GrimoireELK, you need to:

* Install the  `grimoire-elk` Python package, which will pull the `perceval` package and other dependencies with it. It includes the `grimoire_elk` Python module, which knows how to drive perceval to retrieve data from data sources, how to enrich it to produce data suitable to bbe shown in a dashboard, and how to upload everything to ElasticSearch. It includes the `p2o.py` script, as well, which manages `grimoire_elk` from the command line, and will be fundamental for producing the indexes we need for our dashboard.
* Install the `grimoire-kidash` Python package, which includes the `kidash.py` Python script and all dependencies needed for it to work. This scripts will allow us to manage dashboards, visualizations, and other elements in Kibana. We will use it to upload dashboard definitions to produce our dashboard in Kibana.
* Install ElasticSearch and Kibana instances, to store the data and serve the dashboard. Instead of installing your own instances of both, you can use services in the cloud, or already instances, of course.

Let's see the details.

### Installing grimoire-elk and grimoire-kidash

Before installing `grimoire-elk` and `grimoire-kidash`, consider creating a Python3 virtual environnment (see details in First steps with Perceval). In the following, we will assume that we're installing everything in a virtual environment called `grimoireelk`.

Installing both packages is easy: just use pip, for installing from Pypi.

```bash
(grimoireelk) $ pip install grimoire-elk
...
(grimoireelk) $ pip install grimoire-kidash
...
```

This will also install Perceval (for retrieval of data from repositories) and other dependencies in the virtual environment.

### Installing ElasticSearch and Kibana

In case you decide to install ElasticSearch and Kibana yourself, instead of using them as a service, the process is not difficult. Please ensure you're installing at least version 5.1 ob both (as a rule, versions for Kibana and ElasticSearch should be the same if they are to work together).

For ElasticSearch, you can follow its [installation instructions](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html). You will need to have a Java virtual machine installed \(Oracle JDK version 1.8.x is recommended\), The rest is simple: download the installation file from the [ElasticSearch downloads area](https://www.elastic.co/downloads/elasticsearch), and install it, for example by unzipping the zip installation file.

Assuming the installed ElasticSearch directory is `elasticsearch`, to lanuch it you will just run the appropriate command \(no need to run this from the virtual environment\):

```
$ elasticsearch/bin/elasticsearch
```

This will launch ElasticSearch that will listen via its HTTP REST API at `http://localhost:9200`. You can check that everything went well by pointing your web browser to that url, and watching the ElasticSearch welcome message.

For Kibana, you have [installation instructions](https://www.elastic.co/guide/en/kibana/current/setup.html) as well. The process is quite similar: download the installation file from [Kibana dashboards area](https://www.elastic.co/downloads/kibana), and install it for example by unzipping the zip installation file.

Assuming the installed Kibana directory is `kibana`, to launch it, again just run the appropriate command:

```
$ kibana/bin/kibana
```

This should serve a Kibana instance in `http://localhost:5601`. Point your web browser to that url, and you´ll see the Kibana welcome page.

![Kibana welcome page](kibana_welcome.png)

Now, we´re ready to go.

### Alternative: install Kibiter instead of Kibana

Instead of Kibana, you can install [Kibiter](https://github.com/grimoirelab/kibiter), the soft fork of Kibana maintained as a part of GriomoireLab. It includes some goodies, such as customization of titles for visualizations in dashboards, or menus for showing direct access to several dashboards. But if you don't need those good you can work with vanilla Kibana.
