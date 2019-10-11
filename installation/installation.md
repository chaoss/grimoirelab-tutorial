# Installation

There are different ways to install GrimoireLab, they are described below.

## Docker compose

### Requirements
- Git
- Docker
- Docker Compose

### Steps
Once installed the requirements, we can confirm in the command line that everything is up and running by typing the following commands
```bash
$ git --version
git version 2.17.1

$ docker --version
Docker version 19.03.1, build 74b1e89

$ docker-compose --version
docker-compose version 1.24.1, build 4667896
```

Next we can clone the repo [analytics-demo](https://gitlab.com/Bitergia/lab/analytics-demo) , there we will find the docker-compose and the settings files.

```bash
$ git clone https://gitlab.com/Bitergia/lab/analytics-demo.git
$ cd analytics-demo 
```

The settings files will be thoroughly described in the next sections of the tutorial. For the moment, we will briefly highlight the `projects.json` and `setup.cfg`. 

The `projects.json` declares the list of projects we want to analyse, divided per data sources (e.g., git, github, etc.). As we can see, the projects.json includes the project `GrimoireLab`, which data sources are:
- `git`: Git commits
- `github` GitHub issues
- `github:prs`: GitHub pull requests
- `pipermail`: Pipermail messages

The `setup.cfg` contains the details about how to get the project data and how to store it in the platform. To quick start playing with GrimoireLab, we have just to replace `<YOUR_API_TOKEN>` with our [GitHub token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line#creating-a-token).

Next we can start the docker-compose with the following command:
```bash
$ docker-compose up -d
```

Once your containers are all up and running, access to [http://localhost:5601](http://localhost:5601) via any browser. 

## Digital Ocean

TODO

# Troubleshooting

- **Port 3306 already in use**

  This error happens when another process is listening on the port 3306. In case the process is a MySQL running on localhost, you can stop the service (`service mysql stop`)

- **Elasticsearch with red status**

   This error happens when the max virtual memory is too low for Elasticsearch to work properly. To increase the memory, you can execute the following command:
    ```bash 
    sudo sysctl -w vm.max_map_count=262144
    ```