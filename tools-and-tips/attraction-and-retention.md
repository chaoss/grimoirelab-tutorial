# Attraction & retention

Warning: this is work in progress, use at your own risk! 

Scripts and JSON files mentioned here are available from the [tools&tips directory in the GitHub repo](https://github.com/jgbarah/GrimoireLab-training/tree/master/tools-and-tips/scripts).

Use the `enriched_elasticsearch_git_pandas7.py` script as follows:

```python
./enriched_elasticsearch_git_pandas7.py \
  --es https://user:passwd@elasticsearch_url --es_index git \
  --es_out https://user:passwd@elasticsearch_url --es_index_out git_demo \
  --no_verify_certs
```

Then create in Kibana the index pattern `git_demo`, based on the index you just created, and upload to Kibana the following JSON files, which are the searches, visualizations and dashboards:

* `C_dashboard.json`
* `C_visualizations.json`
* `C_searches.json`

And point Kibana to load the dashboard `C_Git_Demo`.