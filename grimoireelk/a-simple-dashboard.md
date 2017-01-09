## Creating a simple dashboard

Creating a dashboard using the tools we just installed is not difficult:

* First, use p2o.py to retrieve the data from the data source, store it in ElasticSearch as a raw index, and then use it to produce the enriched index that will be used to animate the visualizations in the dashboard.
* Upload to Kibiter \(or Kibana\) the configuration needed for the dashboard that will show the enriched index mentioned above.

That's all. After that, you can just point your web browser to the dashboard link, and you are done.

Let's follow the process step by step for a simple dashboard showing information from two git repositories.

### Creating the indexes in ElasticSearch

Let's run `p2o.py` to create the indexes in ElasticSearch. We will create a the enriched index in one step. This index will contain the data used by the Kibana dashboard. As an example, we will produce an index for two git repositories: those of Perceval and GrimoireELK. We will use as index name `git_enrich`, and as ElasticSearch instance the one we have listening at `http://localhost:9200`:

```bash
(grimoireelk) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  git https://github.com/grimoirelab/perceval.git
(grimoireelk) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  git https://github.com/grimoirelab/GrimoireELK.git
```

Now, we should have two new indexes in Kibana: `git_raw`, with the raw data as produced by Perceval, and `git`, with the enriched information, ready to be shown by a Kibana dashobard. You can check both by feeding the following urls to your web browser:

* [http://localhost:9200/git\_raw?pretty=true](http://localhost:9200/git_raw?pretty=true)
* [http://localhost:9200/git?pretty=true](http://localhost:9200/git?pretty=true)

In both cases, you will watch a JSON document with the description of the index.

![](elasticsearch-index.png)

### Uploading the dashboard configuration

Then, the only missing element is a Kibana dashboard with its visualizations. We can use `kidash.py` to upload to Kibana a dashboard definition that we have ready for you in the [git-dashboard.json JSON file](https://raw.githubusercontent.com/jgbarah/GrimoireLab-training/master/grimoireelk/dashboards/git-dashboard.json). Download it to your `/tmp` directory, and run the command:

```
(grimoireelk) $ python3 kidash.py --elastic_url-enrich http://locahost:9200 \
  --import /tmp/git-dashboard.json
```

This should produce the promised dashboard, in all its glory! Point your web browser to [your Kibana instance](http://localhost:5601/), click on `Dashboard` in the top menu, and use the floppy icon \(on the top right list of icons\) to select the `Git` dashboard. Get some popcorn, now you should be able of playing with the dashboard.

![](kibana-dashboard.png)

### Final remarks

In this section you have learned to produce a simple dashboard, using Perceval and GrimoireELK, with the data stored in ElaticSearch, and the dashboard itself in Kibana. It only has information for git repositories, but with a similar procedure, you can produce dashboards for other data sources.

In case you want to try a dashboard for some other repositories, once you're done with this one, you can delete the indexes \(both `git` and `git_raw`\), and produce new indexes with `p2o.py`. For doing this, you can use `curl` and the ElasticsSearch REST HTTP API:

```bash
$ curl -XDELETE http://localhost:9200/git
$ curl -XDELETE http://localhost:9200/git_raw
```

Using the Kibana interface it is simple to modify the dashboard, its visualizations, and produce new dashboards and visualizations. If you are interested, have a look at the [Kibana User Guide](https://www.elastic.co/guide/en/kibana/current/).

`p2o.py` can be used to produce indexes for many other data sources. For example for GitHub issues and pull requests, the magic line is like this \(of course, substitute XXX for your GitHub token\):

```bash
$ p2o.py --enrich --index github_raw --index-enrich github \
  -e http://localhost:9200 --no_inc --debug \
  github --owner grimoirelab --repository perceval \
  -t XXX --sleep-for-rate
```





