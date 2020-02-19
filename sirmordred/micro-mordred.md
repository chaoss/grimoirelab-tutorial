### Micro-mordred via Docker-Compose

### What is Mordred?

- Mordred is the tool used to orchestrate the execution of the GrimoireLab platform, via a configuration file. We can find more details about the sections in the configuration file [here]([https://github.com/chaoss/grimoirelab-sirmordred#general-sections](https://github.com/chaoss/grimoirelab-sirmordred#general-sections)). 

### What is Micro-Mordred?

- Micro-Mordred is a simplified version of Mordred which omits the use of its scheduler. Thus, Micro-Mordred allows to run single Mordred tasks (e.g. raw collection, enrichment) per execution. We can find the implementation of micro-mordred located in [/utils](https://github.com/chaoss/grimoirelab-sirmordred/tree/master/utils/micro.py) directory and it can be executed via command line.


- In this tutorial, we'll try to execute micro-mordred with the help of docker-compose. `Docker-Compose` is a tool for defining and running multi-container Docker applications. As our application in this case (`micro-mordred`), requires instances of ElasticSearch, Kibiter ( a soft-fork of Kibana ) and MariaDB. We'll use `docker-compose` to handle the dependent instances.


### Steps for execution

1. We'll use the following docker-compose configuration to instantiate the required components i.e ElasticSearch, Kibiter and MariaDB. Note that we can omit the `mariadb` section in case you have MySQL/MariaDB already installed in our system. We'll name the following configuration as `docker-config.yml`.

```
elasticsearch:
  restart: on-failure:5
  image: bitergia/elasticsearch:6.1.0-secured
  command: elasticsearch -Enetwork.bind_host=0.0.0.0 -Ehttp.max_content_length=2000mb
  environment:
    - ES_JAVA_OPTS=-Xms2g -Xmx2g
  ports:
    - 9200:9200

kibiter:
  restart: on-failure:5
  image: bitergia/kibiter:secured-v6.1.4-2
  environment:
    - PROJECT_NAME=Development
    - NODE_OPTIONS=--max-old-space-size=1000
    - ELASTICSEARCH_URL=https://elasticsearch:9200
  links:
    - elasticsearch
  ports:
    - 5601:5601
    
mariadb:
  restart: on-failure:5
  image: mariadb:10.0
  expose:
    - "3306"
  ports:
    - "3306:3306"
  environment:
    - MYSQL_ROOT_PASSWORD=
    - MYSQL_ALLOW_EMPTY_PASSWORD=yes
    - MYSQL_DATABASE=test_sh
  command: --wait_timeout=2592000 --interactive_timeout=2592000 --max_connections=300
  log_driver: "json-file"
  log_opt:
      max-size: "100m"
      max-file: "3"
```

You can now run the following command in order to start the execution of individual instances.

```
$ docker-compose -f docker-config.yml up
```

Once you see something similar to the below `log` on your console, it means that you've successfully instantiated the containers corresponding to the required components.

```
elasticsearch_1  | Search Guard Admin v6
elasticsearch_1  | Will connect to 0.0.0.0:9300 ... done
elasticsearch_1  | [2019-05-30T09:38:20,113][ERROR][c.f.s.a.BackendRegistry  ] Not yet initialized (you may need to run sgadmin)
elasticsearch_1  | Elasticsearch Version: 6.1.0
elasticsearch_1  | Search Guard Version: 6.1.0-21.0
elasticsearch_1  | Connected as CN=kirk,OU=client,O=client,L=test,C=de
elasticsearch_1  | Contacting elasticsearch cluster 'elasticsearch' and wait for YELLOW clusterstate ...
elasticsearch_1  | Clustername: bitergia_elasticsearch
elasticsearch_1  | Clusterstate: GREEN
elasticsearch_1  | Number of nodes: 1
elasticsearch_1  | Number of data nodes: 1

...
elasticsearch_1  | Done with success
elasticsearch_1  | $@

...
kibiter_1        | {"type":"log","@timestamp":"2019-05-30T09:38:25Z","tags":["status","plugin:elasticsearch@6.1.4-1","info"],"pid":1,"state":"green","message":"Status changed from red to green - Ready","prevState":"red","prevMsg":"Service Unavailable"}
```

- **Note**: In case you face a memory related error, which might cause the elasticsearch instance not instantiating completely and lead the linked kibiter instance a `Request timeout`. In such a case, try adjusting the `ES_JAVA_OPTS` parameter in the *environment* attribute given in the `docker-config.yml` config file. for eg. ( -Xms1g -Xmx1g )

2. At this point, you should be able to access the *ElasticSearch* instance via `http://admin:admin@localhost:9200` and *Kibiter* instance via `http://admin:admin@localhost:5601` on the browser. (something like below)


<div align="center">
    <img src="https://i.imgur.com/Czunlpr.png">
    <br>
    <p><b>Browser: Kibiter Instance</b></p>
</div>

3. As you can see on the `Kibiter Instance` above, it says `Couldn't find any Elasticsearch data. You'll need to index some data into Elasticsearch before you can create an index pattern`. Hence, in order to index some data, we'll now execute micro-mordred using the following command, which will call the `Raw` and `Enrich` tasks for the Git config section from the provided `setup.cfg` file.

```
$ python3 micro.py --raw --enrich --cfg setup.cfg --backends git
```

The above command requires two files:
  - `setup.cfg`: Contains section of configuration for different components and tools
  - `projects.json`: Contains a list of projects to analyze

Read more about the projects file [here](https://github.com/chaoss/grimoirelab-tutorial/blob/master/sirmordred/projects.md).

We'll (for the purpose of this tutorial) use the files provided in the `/utils` directory, but feel free to play around with the file and their configurations :)

- **Note**: In case the process fails to index the data to the ElasticSearch, check the `.perceval` folder in the home directory; which in this case may contain the same repositories as mentioned in the `projects.json` file. We can proceed after removing the repositories using the following command.

```
$ rm -rf .perceval/repositories/...
```

4. Now, we can create the index pattern and after its successful creation we can analyze the data as per fields. Then, we execute the `panels` task to load the corresponding `sigils panels` to Kibiter instance using the following command.

```
$ python3 micro.py --panels --cfg setup.cfg
```

On successful execution of the above command, we can manage to produce some dashboard similar to the one shown below.

<div align="center">
    <img src="https://i.imgur.com/Of09Voi.png">
    <br>
    <p><b>Dashboard - Git: Areas of Code </b></p>
</div>

- Hence, we have successfully executed micro-mordred with the help of docker-compose.
