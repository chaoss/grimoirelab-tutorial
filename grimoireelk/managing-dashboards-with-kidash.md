## Managing dashboards with kidash

Kibana (or Kibiter, for that matter) offer a nice user interface to create and edit visualizations and dashboards. It allows to save and restore them as well. But if you're interested in backing up all the elements needed to produce a dashboard, you need some tools. That's why we developed kidash. Then, we added some other features to it. And now kidash is our tool of choice to back and restore dashboards with all their elements (visualizations, searches, and index patterns), in the same or in a different Kibana instance.

kidash works by managing the `.kidash` index in ElasticSearch, which is where Kibana stores its configuration. That index includes JSON documents corresponding to all elements in Kibana, from dashboards to index patterns. By retrieving documents from it, you can backup your elements. By creating or changing documents in it, you can create or change elements. kidash allows to save documents from that index in a file, in a comfortable way. That file is in JSON format, which allows for easy edition of it (if you know about how Kibana elements are stored in JSON documents). And kidash can upload the content of those files (be them edited or not) to the same or another Kibana instance.

Kidash is a Python script, kidash.py. It can be installed, with all its dependencies, using pip, as we saw in the [Introduction section in this chapter](installation.md#grimoire-xxx).

### Saving dashboards

If you happen to modify the dashboard, or any of its visualizations, you can save it to a file, using `kidash.py`, either for backup or for uploading to a different Kibana instance. For that, you can get it from the corresponding ElasticSearch instance for our Kibana:

 ```
(grimoireelk) kidash.py -e http://localhost:9200 --dashboard "Git" --export /tmp/dashboard-git.json
 ``` 
