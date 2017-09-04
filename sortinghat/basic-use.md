## Basic use

Let's revisit the dashboard we produced with SortingHat support. We will add some more repositories to it, to have some more complete data, and then we will explore some of the capabilities of SortingHat for merging identities, for adding affiliations and for adapting profiles.

### Adding some more repositories

To have a dashboard with some more complete data, let's add five more repositories to the index we produced in [A dashboard with SortingHat](../grimoireelk/a-dashboard-with-sortinghat.md):

```bash
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/GrimoireELK.git
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/panels.git
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/mordred.git
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/arthur.git

(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/training.git
```










