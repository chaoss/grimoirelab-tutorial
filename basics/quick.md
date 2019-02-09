## Installation for the impatient

So you don't want to read all the details,
you just want to install the stuff and follow on
to other parts of this tutorial?

* If you want to install GrimoireLab Python packages,
and already know about Python virtual environments, `pip`,
and that stuff, go ahead to [Install Python packages](#python).

* If you want to use the GrimoireLab Docker images,
and you already have Docker installed, know about
`docker run` and all that, go ahead to [Run in a Docker container](#docker).

In any case, have a look at the introduction of this chapter,
so that you can get a basic idea of the requirements to run GrimoireLab,
and to the section on What is GrimoireLab, where you will get
a glimpse of the different components in the toolset.

### Install Python packages {#python}

All GrimoireLab packages are pulled by a single Python package,
available from [Pypi](https://pypi.org). If you have a recent version
of Python3, very likely the following will just work
(it is recommended to run it in a virtual environment):

```bash
(gl) % pip install grimoirelab
```

If everything went well, you can just check the version that you installed:

```bash
(gl) % grimoirelab -v
```

And that's it. You can now skip the rest of this chapter
(although it would be a good idea if you at least browse it,
there is useful information in it).

### Run in a Docker container {#docker}

All GrimoireLab packages can also be used from a Docker image, 
that can be pulled and run directly from [Docker Hub](https://hub.docker.com).
Those are exactly the same packages that you get if you install
from [Pypi](https://pypi.org), as shown above.
But in this case, they are already installed on top of a
standard Debian distro, so you can run those directly.

To run that image, just type:

```bash
% docker run -p 127.0.0.1:9200:9200 \
    -p 127.0.0.1:5601:5601 \
    -p 127.0.0.1:3306:3306 \
    -e RUN_MORDRED=NO \
    -t grimoirelab/full
```

This will run the container, with the servers usually needed by
some of GrimoireLab tools (Elasticsearch, Kibiter, MariaDB).
It will also expose the ports for those servers
(Elasticsearch is 9200, Kibiter is 5601, MariaDB is 3306),
so that you can access them from the host machine.
Make sure that you don't have other servers in those ports
in the host machine (for example, an instance of MySQL, which
also runs in 3306).

Once the container is running, you can connect to it,
and launch any GrimoireLab command or program in it:

```bash
$ docker exec -it container_id env TERM=xterm /bin/bash
```

That container can be used also, as such,
to produce a complete dashboard: see
[Mordred in a container](../sirmordred/container.html).

