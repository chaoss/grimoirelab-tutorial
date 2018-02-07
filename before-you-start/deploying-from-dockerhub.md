## Deploying from DockerHub

GrimoireLab can be found, already installed and ready to use, as Docker container images. The image which is likely most useful for a start is [grimoirelab/full](https://hub.docker.com/r/grimoirelab/full), available from DockerHub. It includes all GrimoireLab components, along with the services needed to produce a fully functional GrimoireLab dashboard: Elasticsearch, MariaDB, and Kibiter. By default, the container produces a dashboard for the GrimoireLab project.

For using these container images, ensure you have a recent version of `docker` installed, see [Docker installation instructions](https://docs.docker.com/engine/installation/)). The examples have been tested with 17.x in Debian GNU/Linux,

To try `grimoirelab/full`, just type:

```bash
$ docker run -p 127.0.0.1:5601:5601 \
    -v $(pwd)/credentials.cfg:/mordred-override.cfg \
    -t grimoirelab/full
```

`credentials.cfg` should have a GitHub API token, in  `mordred.cfg` format:

```
[github]
api-token = XXX
```

This will pull the `grimoirelab/full` Docker container image from DockerHub (if it is not already in the local host), and will run it. Upon running it, the container will launch Elasticsearch, MariaDB, and Kibana, so they will be ready when the container launches Mordred to retrieve data from GrimoireLab project repositories, and finally produce a complete dashboard for it.

The resulting dashboard will be available from Kibiter, and you can see it by pointing your browser at http://localhost:5601 . Once you see the dashboard, click on "Overview". You will get something similar to:

![](/assets/dashboard-grimoirelab.png)

What is even more interesting: you can get a shell in the container (after launching it), and run arbitrary GrimoireLab commands (`container_id` is the identifier of the running container, that you can find out with `docker ps`, or by looking at the first line when running the container):

```bash
$ docker exec -it container_id env TERM=xterm /bin/bash
```

The container allows for much more: you can configure the project you want to analyze, have access to the logging created while producing the dashboard, etc. And there are some more ready-to-use container images that could be useful to you. Have a look at the section [Mordred in a container](../mordred/mordred-in-a-container.md) to learn about how to produce dashboards in different ways, and run arbitrary GrimoireLab code, from these containers. More details about the docker images produced by the GrimoireLab projects are available in the [docker/README.md file in the grimoirelab GitHub repository](https://github.com/chaoss/grimoirelab/blob/master/docker/README.md).
