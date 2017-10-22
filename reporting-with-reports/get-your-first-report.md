## Get your first report

Reporting with GrimoireLab Reports is easy. You need to have enriched ElasticSearch indexes, produced by GrimoireELK (see [Producing Kibana dashboards with GrimoireELK](/grimoireelk/producing_kibana_dashboards_with_grimoireelk.md)), and of course, having `grimoirelab-reports` installed. The rest is pretty easy.

For example, to produce a report about Git data in the standard GrimoireLab enriched index in my local ElasticSearch (accesible in the standard [http://localhost:9200](http://localhost:9200) location), you only need to run:

```bash
$ report -d /tmp/report-result -u http://localhost:9200 \
   -n GrimoireLab --data-sources git
```

The report will be produced as `/tmp/report-result/report.pdf`, using `GrimoireLab` as the name of the analyzed project, when presented in the report. 