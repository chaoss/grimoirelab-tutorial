## Obtain CSV from Jenkins enriched indexes in ElasticSearch

To illustrate how to get data from an enriched index (produced using `grimoire_elk`), let's review the script [`enriched_elasticsearch_jenkins.py`](https://github.com/jgbarah/GrimoireLab-training/blob/master/tools-and-tips/scripts/enriched_elasticsearch_jenkins.py). This script will query a Jenkins enriched index, producing a CSV file with some of the fields in it, since a certain number of days.

### Installation

To use it, we can create a new virtual environment for Python, and install the needed modules (including the script) in it.

```bash
$ pyvenv ~/venv
$ source ~/venv/bin/activate
(venv) $ pip install elasticsearch
(venv) $ pip install elasticsearch-dsl
(venv) $ wget https://raw.githubusercontent.com/jgbarah/GrimoireLab-training/master/tools-and-tips/scripts/enriched_elasticsearch_jenkins.py
(venv) $ python enriched_elasticsearch_jenkins.py --help
...
```

The last command should show the script help banner.

### Execution

To use it, we will specify the url for the ElasticSearch instance we will use, the name of the Jenkins enriched index, and (optionally) a number of days (since when we want to get entries). If days are not specified, the script will produce entries for the last 90 days. Let's try it:

```bash
(venv) $ python enriched_elasticsearch_jenkins.py --es elastic_url \
  --es_index jenkins --days 2 > /tmp/jenkins.csv
```

The resulting file `/tmp/jenkins.csv` will be like:

```
job_build,build_date,duration(ms),result,builtOn,build,branch,loop,job_name
ha-master/108,2017-02-23T06:42:30.575000+00:00,8800991,FAILURE,pod2,108,master,ha,ha-master
ha-rel/107,2017-02-23T01:20:38.197000+00:00,6360746,FAILURE,pod2,107,rel,ha,ha-rel
...
```

The first line is the CSV header, and then we have one entry per line. Each entry shows several fields in the ElasticSearch document corresponding to a job build.

### Some details

Let's have a look at some regions of the code of the script.

```python
es = elasticsearch.Elasticsearch(
    [args.es],
    verify_certs=args.verify_certs
    )
```

This will create an ElasticSearch object, which will be used to connect to ElasticSearch. As parameters, we pass a list of the urls to access the intended index (in our case, only one), and a parameter which will be true in case we don't want to verify SSL certificates (for instance, if they are not signed by the right UA, but we know they are reliable enough).

```python
request = elasticsearch_dsl.Search(using=es, index=args.es_index)
request = request.filter('range',
                        build_date={'from': datetime.datetime.now() - datetime.timedelta(days=args.days)})
request = request.sort('-build_date')
```

The above code creates the request we will use, in several stages. First, we produce a Search request, specifying the index we want to query. Then, we filter it for a certain time period (since some days ago until now). Finally, we sort the results by build date, in descenting order.

Once the request is complete, we'ready to execute it using the scan method, which can retrieve large collections of items from an index:

```python
response = request.scan()
print("job_build,build_date,duration(ms),result,builtOn,build,branch,loop,job_name")
for job in response:
    print("{},{},{},{},{},{},{},{},{}".format(
        job['job_build'], job['build_date'],
        job['duration'], job['result'],
        job['builtOn'], job['build'],
        job['branch'], job['loop'], job['job_name']
        ))
```

Once executed, we will just loop through the result, printing one line of the CSV file for each iteration. Before that, we will write the header of the CVS file, with names for all the fields to show.