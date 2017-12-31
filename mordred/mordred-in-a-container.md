## Mordred in a container

To produce a dashboard with Mordred, you can also use some containers, available from DockerHub, ready to work:

* [grimoirelab/installed](https://hub.docker.com/r/grimoirelab/installed/): includes all GrimoireLab components, and after booting up, it runs Mordred by default. This image does not include Elasticsearch, Kibiter or MariaDB: they shouldl be available in the host where it is run, in the standard ports.

* [grimoirelab/full](https://hub.docker.com/r/grimoirelab/full). Includes GrimoireLab and runs Mordred, as `grimoirelab/installed` does, but also includes all services needed to produce a dashboard: Elasticsearch, MariaDB, and Kibiter.

`grimoirelab/full` is the best option if you just want a painless experience of building a dashboard, and don't mind pulling a large docker image. `grimoirelab/installed` is smaller, and more suitable for using GrimoireLab if you already have Elasticsearch, MariaDB and Kibiter available in your host or somewhere else.

For using these container images, ensure you have a recent version of `docker` installed, see [Docker installation instructions](https://docs.docker.com/engine/installation/)). The examples have been tested with 17.x in Debian GNU/Linux,

### Running grimoirelab/full

To try it this container image, just run it as follows:

```bash
$ docker run -p 127:0.0.1:5601:5601 \
    -v $(pwd)/mordred-local.cfg:/mordred-local.cfg \
    -t grimoirelab/full
```

`mordred-local.cfg` should have a GitHub API token (see [Personal GitHub API tokens](https://github.com/blog/1509-personal-api-tokens)), in a `mordred.cfg`
format:

```
[github]
api-token = XXX
```

This will pull the `grimoirelab/full` Docker container image from DockerHub (if it is not already in the local host), and will run it. Upon running it, the container will launch Elasticsearch, MariaDB, and Kibana, so they will be ready when the container launches Mordred to produce a complete GrimoireLab dashboard. With the default configuration, a dashboard for the GrimoireLab project will be produced. Once produced, you can just point your browser to http://localhost:5601 and voila.

The `docker run` command line above exposed port 5601 in the container to be reachable from the host, as  `localhost:5601`. If you omit "127:0.0.1:", it will be reachable to any other machine reaching your host, so be careful: by default there is no access control in the Kibiter used by this container.

That line used the `mordred-local.cfg` file for the configuration for Mordred. In fact, this will be the third configuration file in a chain for Mordred. The other two can be substituted at runtime for different
configurations. The first one, `/mordred.cfg`, has the general configuration for producing a dashboard for the GrimoireLab project. It can be adapted to produce a dashboard for other projects. The second one, `/mordred-full.cfg`, has the configuration for reaching the services used by the container (ElasticSearch, MariaDB, Kibiter), and is likely that you don't need to change it except if you want to use some external service instead of those provided by the container.

A slightly different command line is as follows:

```bash
$ docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:5601:5601 \
    -v $(pwd)/logs:/logs \
    -v $(pwd)/mordred-local-full-jgb.cfg:/mordred-local.cfg \
    -t grimoirelab/full
```

This one will expose also port `9200`, which corresponds to Elasticsearch. This allows direct queries to the indexes stored in it. In addition, it also mounts a local directory (`logs`) so that the container writes Mordred logs in it.

By default, Elasticsearch will store indexes within the container image, which means they are not persistent if the image shuts down. But you can mount a local directory for Elasticsearch to write the indexes in it. this way they will be available from one run of the image to the next one. For example, to let Elasticsearch use directory `es-data` to write the indexes:

```bash
$ docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:5601:5601 \
    -v $(pwd)/logs:/logs \
    -v $(pwd)/mordred-local-full-jgb.cfg:/mordred-local.cfg \
    -v $(pwd)/es-data:/var/lib/elasticsearch \
    -t grimoirelab/full
```

**Warning** When Mordred is done, the container stays forever (well, in fact for a long number of days), so that Kibana is still available to produce the dashboard for your browser. When you want to kill the container, it is not enough to just type `<CTRL> C`, sice that will only kill the shell, but the services on the background will stay. You will need to use `docker kill` to kill the container.


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

