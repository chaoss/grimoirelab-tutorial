## Managing dashboards with kidash

Kibana (or Kibiter, for that matter) offer a nice user interface to create and edit visualizations and dashboards. It allows to save and restore them as well. But if you're interested in backing up all the elements needed to produce a dashboard, you need some tools. That's why we developed Kidash. Then, we added some other features to it. And now Kidash is our tool of choice to back and restore dashboards with all their elements (visualizations, searches, and index patterns), in the same or in a different Kibana instance.

Kidash works by managing the `.kibana` index in ElasticSearch, which is where Kibana stores its configuration. That index includes JSON documents corresponding to all elements in Kibana, from dashboards to index patterns. By retrieving documents from it, you can backup your elements. By creating or changing documents in it, you can create or change elements. kidash allows to save documents from that index in a file, in a comfortable way. That file is in JSON format, which allows for easy edition of it (if you know about how Kibana elements are stored in JSON documents). And kidash can upload the content of those files (be them edited or not) to the same or another Kibana instance.

Kidash provides a Python script, `kidash`. It can be installed, with all its dependencies, using pip, as we saw in the [section on Installing GrimoireLab](/before-you-start/installing-grimoirelab.md).

### Saving dashboards

You can save a dashboard, with all its components, to a file, either for backup or for later uploading to a different Kibana instance. You will need access to the ElasticSearch instance that your Kibana is using, because kidash will be reading its `.kibana` index. Assuming that Kibana is in localhost, at port 9200, and that you want to backup the dashboard named "Git" to the file `/tmp/dashboard-git.json`, just run (from the virtual environment where you installed `grimoire-kidash`):


```bash
(grimoireelk) kidash -e http://localhost:9200 --dashboard "Git" --export /tmp/dashboard-git.json
``` 

You can learn the name of the dashboard by looking at its top left corner, or by noting the name you use when opening it in Kibana. If the name includes spaces, use "-" instead. For example, for a dashboard named "Git History", use the line:

```bash
(grimoireelk) kidash -e http://localhost:9200 --dashboard "Git-History" \
  --export /tmp/dashboard-git.json
``` 

If you open the file created, you will see it is written in JSON format. In fact, it is a dictionary with one entry per kind of element (dashboards, visualizations, searches, index patterns). For each kind of element, you will find a list of the saved elements, as dictionaries with their characteristics. These are the same you can read in Kibana (only for dashboards, visualizations, and searches) in the "Management | Saved Objects" menu entry, if you edit one of the elements. kidash takes care of, given the name of the dashborad, find recursively the other elements needed to draw it.

### Restoring dashboards

We already restored a dashboard in the [section on creating a simple dashboard](a-simple-dashboard.md#uploading-dashboard). We can restore from any file created with kidash. Assuming we have that file as `/tmp/dashboard-git.json`, we need to know the link to the ElasticSearch REST interface (same as for backing up). The format is, for example, as follows:

```bash
(grimoireelk) $ kidash --elastic_url-enrich http://localhost:9200 \
  --import /tmp/git-dashboard.json
```

This will restore all elements in the file, overwritting, if needed, elements with the same name in the corresponding Kibana instance (in fact, in the corresponding ElasticSearch `.kibana` index). Therefore, beware: restoring a JSON file with kidash may destroy your elements, because they may be overwritten by others in the file. Remember to backup before running the command.

### Other options

Kidash has some more options. For a complete listing, use the `--help` argument:

```bash
(grimoireelk) $ kidash --help
```
