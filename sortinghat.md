# SortingHat

We already [built an index with SortingHat support](/grimoireelk/a-dashboard-with-sortinghat.md), and produced a dashboard showing it. But there is still a lot of SortingHat to learn, if we want to use all of its capacities. In this chapter we will learn how to use SortingHat in combination to other GrimoireLab tools (mainly Perceval and `p2o.py`). For a more complete guide to SortingHat, read the [SortingHat README](https://github.com/grimoirelab/sortinghat/blob/master/README.md).

We will start by adding some more repositories to the index, to have some more complete data. Then we will use it to explore the capabilities of SortingHat for merging identities, for adding affiliations and for adapting profiles.

```bash
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/GrimoireELK.git
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/panels.git
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/mordred.git
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/arthur.git
(sh) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/training.git
```

When we run `p2o.py` in all these cases, it uses Perceval to retrieve data from the corresponding git repositories, producing a raw index (`git_raw`). Based on it, `p2o.py` later produces the enriched index (`git`). Here is where SortingHat enters the game. Each new identity that `p2o.py` finds while enriching the raw index (in the case of git repositories, usually email addresses and names) is added to SortingHat. When looking in the SortingHat database we will see all these identities. Additionally, with the information stored in SortingHat, `p2o.py` produces some fields in the enriched index, such as the organziation or the name to show in the dashboard for each developer.

Therefore, SortingHat controls how identities are matched to people, and people to organizations. It also controls how people are shown in the indexes. Let's see how.
