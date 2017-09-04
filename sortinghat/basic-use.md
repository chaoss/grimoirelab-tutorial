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

### Tables generated with SortingHat

When we run `p2o.py` in all these cases, it has been using Perceval to retrieve data from the corresponding git repositories, and producing a raw index (`git_raw`) with all the metadata in them. After that, it uses that raw index to produce the enriched index, and there is where SortingHat enters the game. Each new identity that `p2o.py` finds (in the case of git repositories, usually email addresses and names) is added to SortingHat. Therefore, we will see how the SortingHat database has all the identities found in the repositories that we included in the index. Additionally, with the information stored in SortingHat, `p2o.py` produces some fields in the index, such as the organziation or the name to show in the dashboard for each developer.

But before looking for that data in the database, let's see which tables it has. For that, we just query MySQL:

```bash
$ mysql -u jgb -pXXX -e 'SHOW TABLES;' sh_grimoirelab
...
| countries             |
| domains_organizations |
| enrollments           |
| identities            |
| matching_blacklist    |
| organizations         |
| profiles              |
| uidentities           |
+-----------------------+
```

Let's summarize the aim of each table:

* `identities`: identities found in repositories. Each identity is a tuple composed of a unique identifier (a hash of the other fields, `id`), a name (`name`), an email address (`email`), a username (`username`), the source where the identity was found (`source`, with tags identifying the kind of repository where the identity was found, such as `git`, `bugzilla` or `github`), and the merged identity to which it corresponds (`uuid`). All fields in the tuple except for `uuid` a inmutable: they never change during the live of a SortingHat database. The `uuid` is used to merge identities that correspond to the same person: each person should have a single `uuid`, and that `uuid` will be in this table for all the identities corresponding to that person. In fact, the `uuid` is the `id` of one of those identities. The name, the email address and the username are the data composing the identity. For example, email addresses usually have `name` and `email` (such as "Jesus Gonzalez <jgb@bitergia.com>), while `username` is `NULL`. GitHub accounts usually have `name` and `username` (such as "Jesus Gonzalez, jgbarah"), with `email` as `NULL`. The `uuid` will change during the life of the database as new identities for the same person are found, or as wrong merged identities are identified (and broken). A large part of the maintenance of a SortingHat database consists of dealing with `uuid` in this table, while merging and unmerging identities.


* `countries`

* `domains_organizations`

* `enrollments`



* `matching_blacklist`

* `organizations`

* `profiles`

* `uidentities`




