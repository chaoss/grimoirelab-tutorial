## Setting up the environment

To set up the complete environment to produce a Kibana-based dashboard based on GrimoireELK, you need to:

* Install the`grimoire_elk`Python module, which will pull the `perceval`module and other dependencies with it. It includes the `p2o.py` script, as well.
* Install the `kidash.py` Python script, to manage Kibana dashboards and visualizations.
* Install ElasticSearch and Kibana instances, to store the data and serve the dashboard. Instead of installing your own instances of both, you can use services in the cloud, or already instances, of course.

Let's see the details.

### Installing grimoire\_elk and kidash.py

Before installing `grimoire_elk` and `kidash.py`, consider creating a Python3 virtual environnment \(see details in First steps with Perceval\). In the following, we will assume that we're installing everything in a virtual environment called `grimoireelk`.

Installing `grimoire_elk`is easy: just use pip, for installing from Pypi.

```bash
(grimoireelk) $ pip install grimoire_elk
```

This will also install Perceval \(for retrieval of data from repositories\) and other dependencies in the virtual environment.

For now, `kidash.py`has to be installed from the GrimoireELK git repository, either by directlry copying it, or by cloning the git repository llocally, and then using it from there. For copying it, just download the appriate url, for example by using curl:

```bash
$ curl -O https://raw.githubusercontent.com/grimoirelab/GrimoireELK/master/utils/kidash.py
```

For using the script from a clone of the repository, just clone it:

```bash
$ git clone https://github.com/grimoirelab/grimoireelk.git
```

This will create the `grimoireelk` directory, with the sources of `grimoire_elk` and other goodies, among them, `kidash.py` in the `utils` directory.

### Installing ElasticSearch and Kibana

In case you decide to install ElasticSearch and Kibana yourself, instead of using them as a service, the process is not difficult.

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

