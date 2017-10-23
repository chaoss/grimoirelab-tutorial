## Supporting systems

This section shows how to install the packages that support GrimoireLab. This has been tested in Debian GNU/Linux 9.0, for other systems your mileage may vary.

The packages to install are:

* Python3: GrimoireLab is written in Python3, so you need to have it installed. At least Python 3.5 is recommended, but older versions could work.
* Programas for retrieving data from data sources. In some cases, some programs will be needed when retrieving data, since GrimoireLab/Perceval will use them. The most common case is `git`, for the git GrimoireLab/Peerceval backend.
* ElasticSearch: if you want to store raw or enriched GrimoireLab indexes (produced by GrimoireELK).
* Kibana: if you want to visualize enriched indexes (produced by GrimoireELK). For example, because you want to browse GrimoireLab dashboards.
* MariaDB: if you want to use SortingHat for identity management.

### Installing Python3

Python3 is a standard package in Debian, so it is easy to install:

```
% sudo apt-get install python3
```

Once installed, you can check the installed version:

```
% python3 --version
```

For installing some other Python modules, including GrimoireLab modules, you will need `pip` for Python3, which is also available in Debian:

```
% sudo apt-get install python3-pip
```

More information about installing Python3 in other platforms is available in [Properly installing Python](http://docs.python-guide.org/en/latest/starting/installation/).

### Installing git

If you are retrieving data from git repositories, you will need git installed. Pretty simple:

```
$ sudo apt-get install git-all
```

More information about installing git in other platforsm is available in [Getting Started - Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

### Installing ElasticSearch and Kibana

In case you decide to install ElasticSearch and Kibana yourself, instead of using them as a service, the process is not difficult. Please ensure you're installing at least version 5.1 of both of them (as a rule, versions for Kibana and ElasticSearch should be the same if they are to work together).

For ElasticSearch, you can follow its [installation instructions](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html). You will need to have a Java virtual machine installed \(Oracle JDK version 1.8.x is recommended\), The rest is simple: download the installation file from the [ElasticSearch downloads area](https://www.elastic.co/downloads/elasticsearch), and install it, for example by unzipping the zip installation file.

Assuming the installed ElasticSearch directory is `elasticsearch`, to launch it you will just run the appropriate command \(no need to run this from the virtual environment\):

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

### Installing ElasticSearch and Kibana from a Docker container

Instead of following the installation instructions mentioned above, you can also install ElasticSearch and Kibana as a Docker container, by using pre-composed images. For example:

```bash
$ docker run -d -p 9200:9200 -p 5601:5601 nshou/elasticsearch-kibana
```

Then you can connect to Elasticsearch by localhost:9200 and its Kibana front-end by localhost:5601. See [details about these Docker images in DockerHub](https://hub.docker.com/r/nshou/elasticsearch-kibana/)


### Alternative: install Kibiter instead of Kibana

Instead of Kibana, you can install [Kibiter](https://github.com/grimoirelab/kibiter), the soft fork of Kibana maintained as a part of GrimoireLab. It includes some goodies, such as customization of titles for visualizations in dashboards, or menus for showing direct access to several dashboards. But if you don't need those goodies you can work with a vanilla Kibana.

### Installing MariaDB

If you are going to use SortingHat, you will need a database. Currently, MySQL-like databases are supported. In our case, we will use MariaDB. Installing it in Debian is easy:

```
sudo apt-get install mariadb-server
```

That's it, that's all.