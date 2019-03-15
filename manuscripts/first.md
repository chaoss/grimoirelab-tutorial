## Reporting with Manuscripts

[Manuscripts](https://github.com/chaoss/grimoirelab-manuscripts) is the GrimoireLab tool
to produce reports.
It uses data from GrimoireLab indexes in ElasticSearch, and produces PDF documents with charts and tables, useful for getting an idea of how the project is performing.

### Get your first report

Reporting with GrimoireLab Manuscripts is easy. You need to have enriched ElasticSearch indexes, produced by GrimoireELK (see [Producing Kibana dashboards with GrimoireELK](/grimoireelk/intro.md)) or Mordred (see [Mordred: orchestrating everything](/mordred/intro.md)), and of course, having `grimoirelab-manuscripts` installed. The rest is pretty easy.

For example, to produce a report about Git data in the standard GrimoireLab enriched index in my local ElasticSearch (accessible in the standard [http://localhost:9200](http://localhost:9200) location), you only need to run:

```bash
(gl) $ manuscripts -d /tmp/reports -u http://localhost:9200 \
   -n GrimoireLab --data-sources git
```

The report will be produced as `/tmp/reports/report.pdf`, using `GrimoireLab` as the name of the analyzed project, when presented in the report.

> _Note:_ This requires pdflatex to be installed, the instructions for which can be found [here](https://gist.github.com/rain1024/98dd5e2c6c8c28f9ea9d). If you get an error about 'CJKutf8.sty' not being found, check [this](https://tex.stackexchange.com/questions/125843/how-to-install-cjk-font-to-ubuntu-latex) out.
