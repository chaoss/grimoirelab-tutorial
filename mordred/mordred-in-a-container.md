## Mordred in a container

To produce a dashboard with Mordred, you can also use some containers, available from DockerHub, ready to work:

* [grimoirelab/installed](https://hub.docker.com/r/grimoirelab/installed/): includes all GrimoireLab components, and after booting up, it runs Mordred by default. This image does not include Elasticsearch, Kibiter or MariaDB: they shouldl be available in the host where it is run, in the standard ports.

* [grimoirelab/full](https://hub.docker.com/r/grimoirelab/full). Includes GrimoireLab and runs Mordred, as `grimoirelab/installed` does, but also includes all services needed to produce a dashboard: Elasticsearch, MariaDB, and Kibiter.

`grimoirelab/full` is the best option if you just want a painless experience of building a dashboard, and don't mind pulling a large docker image. `grimoirelab/installed` is smaller, and more suitable for using GrimoireLab if you already have Elasticsearch, MariaDB and Kibiter available in your host or somewhere else.

For using these container images, ensure you have a recent version of `docker` installed, see [Docker installation instructions](https://docs.docker.com/engine/installation/)). The examples have been tested with 17.x in Debian GNU/Linux,

### Running grimoirelab/full


### Running grimoirelab/installed

For running the `grimoirelab/installed` docker image, first set up the supporting systems in your host, as detailed in the [Supporting systems](before-you-start/supporting-systems.md) section.  Finally, compose a Mordred configuration file with credentials and references the supporting system. For example:

```
[es_collection]
url = http://localhost:9200
user =
password =

[es_enrichment]
url = http://127.0.0.1:9200
user =
password =

[sortinghat]
host = localhost
user = jgb
password = XXX
database = grimoirelab_sh

[github]
api-token = a98aaef1910d8bf4d875c681e030eed09e409d46
```

The first lines specify how to access Elasticsearch (the link to its REST API, and credentials) for managing both raw (`es_collection`) and enriched (`es_enrichment`) indexes. The values in this example are the default ones if you just install Elasticsearch as explained in the Supporting Systems section.

Then, there are some lines for the SortingHat database: they should be the location (`localhost` in this case) of MariaDB or MySQL, credentials for accesing it, and the name of the SortingHat database (schema) you want to use (if it does not exist, it will be created).

The last two lines specify your GitHub user token, which is needed to access the GitHub API. This is because the default behavior of the container is to visit GitHub as one of the data sources to collect.
 
Now, just run the container as:

```bash
$ docker run --net="host" \
  -v $(pwd)/mordred-local.cfg:/mordred-local.cfg \
  grimoirelab/installed
```

`mordred-local.cfg` is the name of the Mordred configuration file mentioned above.

This will pull the image from [DockerHub](http://dockerhub.com), and run it allowing it to "see" the network ports of the host. This way, GrimoireLab tools running in the contaniner will be able of connecting to Elasticsearch to produce and consume indexes, and MariaDB or MySQQL to manage the SortingHat database.

If run as above, the container will run Mordred, which in turn will run the GrimoireLab tools needed to produce a standard dashboard for the GrimoireLab project.

