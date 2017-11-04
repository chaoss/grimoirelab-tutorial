## Supporting systems

This section shows how to install the packages that support GrimoireLab. This has been tested in Debian GNU/Linux 9.0, for other systems your mileage may vary.

The packages to install are:

* Python3: GrimoireLab is written in Python3, so you need to have it installed. At least Python 3.5 is recommended, but older versions could work.
* Programas for retrieving data from data sources. In some cases, some programs will be needed when retrieving data, since GrimoireLab/Perceval will use them. The most common case is `git`, for the git GrimoireLab/Peerceval backend.
* ElasticSearch: if you want to store raw or enriched GrimoireLab indexes (produced by GrimoireELK).
* Kibiter: if you want to visualize enriched indexes (produced by GrimoireELK). For example, because you want to browse GrimoireLab dashboards. You can also install vanilla Kibana (Kibiter is a soft fork from Kibana), although in that case maybe some of the functionality will not be available.
* MariaDB: if you want to use SortingHat for identity management.

### Installing Python3

Python3 is a standard package in Debian, so it is easy to install:

```bash
$ sudo apt-get install python3
```

Once installed, you can check the installed version:

```bash
$ python3 --version
```

For installing some other Python modules, including GrimoireLab modules, you will need `pip` for Python3. For using `venv` virtual environments, you will also need `ensurepip`. Both are available in Debian and derivatives as packages `python3-pip` and `python3-venv`:

```bash
$ sudo apt-get install python3-pip
$ sudo apt-get install python3-venv
```

More information about installing Python3 in other platforms is available in [Properly installing Python](http://docs.python-guide.org/en/latest/starting/installation/). In addition, you can also check information on [how to install pip](https://pip.pypa.io/en/stable/installing/).

### Installing git

If you are retrieving data from git repositories, you will need git installed. Pretty simple:

```bash
$ sudo apt-get install git-all
```

More information about installing git in other platforsm is available in [Getting Started - Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

### Installing ElasticSearch

In case you decide to install ElasticSearch and Kibiter or Kibana yourself, instead of using them as a service, the process is not difficult. Please ensure you're installing at least version 5.1 of both of them. As a rule, versions for Kibana and ElasticSearch should be the same if they are to work together. If you are installing Kibiter, you can find out the latest release of it (see below), and install the corresponding ElasticSearch version.

For installing ElasticSearch you can follow its [installation instructions](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html). You will need to have a Java virtual machine installed \(Oracle JDK version 1.8.x is recommended\), The rest is simple: download the installation file from the [ElasticSearch downloads area](https://www.elastic.co/downloads/elasticsearch), and install it, for example by unzipping the zip installation file.

Assuming the installed ElasticSearch directory is `elasticsearch`, to launch it you will just run the appropriate command \(no need to run this from the virtual environment\):

```bash
$ elasticsearch/bin/elasticsearch
```

This will launch ElasticSearch that will listen via its HTTP REST API at `http://localhost:9200`. You can check that everything went well by pointing your web browser to that url, and watching the ElasticSearch welcome message.

### Installing Kibiter

For installing Kibiter, grab the version you want from the [Kibiter releases at GitHub](https://github.com/grimoirelab/kibiter/releases). You will need the `.tar.gz` or `.zip` file (if available) for your version of choice. Then, follow the [Kibana installation instructions](https://www.elastic.co/guide/en/kibana/current/install.html) (see below for a summary of those instructions). Remember that you will need a version of ElasticSearch matching the version of Kibiter.

Once you are done, point your browser to [http://localhost:5601](http://localhost:5601) (asuming Kibana was installed in your local machine, using the default port), and you'll get something like:

![](/assets/Screenshot-2017-11-4 Bitergia Analytics.png)

### Installing Kibana

You can install Kibana instead of Kibiter. Maybe you will lose some functionality, but still most of the dashboards will likely work. If this is your case, follow the [Kibana installation instructions](https://www.elastic.co/guide/en/kibana/current/setup.html). The process is similar to ElasticSearch: download the installation file from [Kibana dashboards area](https://www.elastic.co/downloads/kibana), and install it for example by unzipping the zip installation file.

Assuming the installed Kibana directory is `kibana`, to launch it, again just run the appropriate command:

```bash
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

```bash
$ sudo apt-get install mariadb-server
```

That's it, that's all.