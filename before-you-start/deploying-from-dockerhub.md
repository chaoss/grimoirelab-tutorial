## Deploying from DockerHub

GrimoireLab is available as Docker container images. The image which is likely most useful for a start is [grimoirelab/full](https://hub.docker.com/r/grimoirelab/full), available from DockerHub. It includes all GrimoireLab components, along with the services needed to produce a fully functional GrimoireLab dashboard: Elasticsearch, MariaDB, and Kibiter. By default, the container produces a dashboard for the GrimoireLab project.

To try it, you can just type (assuming you have a recent version of docker installed in your system):

```bash
$ docker run -p 127:0.0.1:5601:5601 \
    -v $(pwd)/mordred-local.cfg:/mordred-local.cfg \
    -t grimoirelab/full
```

`mordred-local.cfg` should have a GitHub API token, in  `mordred.cfg` format:

```
[github]
api-token = XXX
```

This will pull the `grimoirelab/full` Docker container image from DockerHub
(if it is not already in the local host), and will run it.
Upon running it, the container will launch Elasticsearch, MariaDB, and Kibana,
so they will be ready when the container launches Mordred to retrieve data from GrimoireLab project repositories, and finally produce a complete dashboard for it.

The resulting dashboard will be available from Kibiter, and you can see it by pointing your browser at http://localhost:5601 . Once you see the dashboard, click on "Overview". You will get something similar to:

![](/assets/dashboard-grimoirelab.png)

What is even more interesting: you can get a shell in the container (after launching it), and run arbitrary GrimoireLab commands (`container_id` is the identifier of the running container, that you can find out with `docker ps`):

```bash
$ docker exec -it container_id env TERM=xterm /bin/bash
```

The container allows for much more: you can configure the project you want to analyze, have access to the logging created while producing the dashboard, etc.  Have a look at the section [Mordred in a container](../mordred/mordred-in-a-container.md), and to  [grimoirelab/docker/README.md](https://github.com/grimoirelab/grimoirelab/blob/master/docker/README.md) for more detailed instructions.
