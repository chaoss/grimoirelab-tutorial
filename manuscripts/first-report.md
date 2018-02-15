## Get your first report

Reporting with GrimoireLab Manuscripts is easy. You need to have enriched ElasticSearch indexes, produced by GrimoireELK (see [Producing Kibana dashboards with GrimoireELK](/grimoireelk/intro.md)) or Mordred (see [Mordred: orchestrating everything](/mordred/intro.md)), and of course, having `grimoirelab-manuscripts` installed. The rest is pretty easy.

For example, to produce a report about Git data in the standard GrimoireLab enriched index in my local ElasticSearch (accesible in the standard [http://localhost:9200](http://localhost:9200) location), you only need to run:

```bash
$ manuscripts -d /tmp/reports -u http://localhost:9200 \
   -n GrimoireLab --data-sources git
```

The report will be produced as `/tmp/reports/report.pdf`, using `GrimoireLab` as the name of the analyzed project, when presented in the report.