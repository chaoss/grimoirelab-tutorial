---
layout: default
title: Troubleshooting
nav_order: 3
parent: Getting-started
---

# Troubleshooting

If something goes wrong during the setup, run the docker-compose command without
the `-d`. That will allow you to see all the logs in regards to the build.

```console
grimoirelab/docker-compose$ docker-compose up
```

### Port already in use

It may also happen that the port, 5601, is already allocated to some other
container. So running docker-compose will lead to the following error

```console
WARNING: Host is already in use by another container
```

In order to fix it, you need to see which container is using that port and kill
that container.

```console
$ docker container ls   #View all running containers
CONTAINER ID   IMAGE                                                     COMMAND                  CREATED         STATUS                     PORTS                                                 NAMES
01f0767adb47   grimoirelab/hatstall:latest                               "/bin/sh -c ${DEPLOY…"   2 minutes ago   Up 2 minutes               0.0.0.0:8000->80/tcp, :::8000->80/tcp                 docker-compose_hatstall_1
9587614c7c4e   bitergia/mordred:latest                                   "/bin/sh -c ${DEPLOY…"   2 minutes ago   Up 2 minutes (unhealthy)                                                         docker-compose_mordred_1
c3f3f118bead   bitergia/kibiter:community-v6.8.6-3                       "/docker_entrypoint.…"   2 minutes ago   Up 2 minutes               0.0.0.0:5601->5601/tcp, :::5601->5601/tcp             docker-compose_kibiter_1
d3c691acaf7b   mariadb:10.0                                              "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes               3306/tcp                                              docker-compose_mariadb_1
f5f406146ee9   docker.elastic.co/elasticsearch/elasticsearch-oss:6.8.6   "/usr/local/bin/dock…"   2 minutes ago   Up 2 minutes               0.0.0.0:9200->9200/tcp, :::9200->9200/tcp, 9300/tcp   docker-compose_elasticsearch_1
$ docker rm -f c3f3f118bead          #c3f3f118bead is the container that is using port 5601.
```

### Empty dashboard or visualization

Usually this is a matter of time for GrimoireLab to fetch the data from the
configured data source. However It may happen that some <span style="color:
red">filters</span> might be activated. You can see whether a filter is active
by looking at the filter bar as shown in the following screenshot or the <span
style="color: #2f4bff">time window</span>.

![filter](./assets/filters.png)