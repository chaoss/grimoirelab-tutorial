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

But before looking for that data in the database, let's see which tables it has. For that, we just query MySQL \(see [A dashboard with SortingHat](../grimoireelk/a-dashboard-with-sortinghat.md) for details on the database\):

```bash
$ mysql -u user -pXXX -e 'SHOW TABLES;' sh_grimoirelab
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

* `identities`: identities found in repositories, and to which unique (merged) identity correspond each of them.
* `uidentities`: unique (merged)) identities.
* `profiles`: information to show in the dashboard for a unique identity.
* `organizations`: organziations to which unique identities may be affiliated.
* `enrollments`: relationship between unique identities and organizations.
* `countries`: countries which can be used in profiles.
* `domains_organizations`: email domains for organizations, used to infer affiliation relationships.
* `matching_blacklist`: identities that should not be merged with others

Now, let's visit the most important of those, exploring the data we have for them in our database.

### The identities and the uidentities tables

Each identity in the `identity` table is a tuple composed of the following fields:

* a unique identifier (a hash of the other fields, `id`)
* a name (`name`), an email address (`email`)
* a username (`username`)
* the source where the identity was found (`source`, with tags identifying the kind of repository where the identity was found, such as `git`, `bugzilla` or `github`)
* the merged identity to which it corresponds (`uuid`)

All fields in the tuple except for `uuid` a inmutable: they never change during the live of a SortingHat database. The `uuid` is used to merge identities that correspond to the same person: each person should have a single `uuid`, and that `uuid` will be in this table for all the identities corresponding to that person. In fact, the `uuid` is the `id` of one of those identities. The name, the email address and the username are the data composing the identity.

For example, email addresses usually have `name` and `email` (such as "Jesus Gonzalez <jgb@bitergia.com>), while `username` is `NULL`. GitHub accounts usually have `name` and `username` (such as "Jesus Gonzalez, jgbarah"), with `email` as `NULL`. The `uuid` will change during the life of the database as new identities for the same person are found, or as wrong merged identities are identified (and broken). A large part of the maintenance of a SortingHat database consists of dealing with `uuid` in the `identies table, while merging and unmerging identities.

Let's see what do we have in our SortingHat database (in the output of `mysql` below, I have trimmed the hashes for `id` and `uuid` to 7 chars):

```bash
mysql -u user -pXXX -e 'SELECT * FROM identities;' shdb
| id      | name                           | email                                | username | source | uuid    | 
| 0cac4ef | Quan Zhou                      | quan@bitergia.com                    | NULL     | git    | 0cac4ef |
| 0ef1c4a | Jesus M. Gonzalez-Barahona     | jgbarah@gmail.com                    | NULL     | git    | 0ef1c4a |
| 11cc034 | quan                           | zhquan7@gmail.com                    | NULL     | git    | 11cc034 |
| 35c0421 | Alberto Martín                 | alberto.martin@bitergia.com          | NULL     | git    | 35c0421 |
| 37a8187 | Alberto Martín                 | albertinisg@users.noreply.github.com | NULL     | git    | 37a8187 |
| 3ca4e85 | Daniel Izquierdo Cortazar      | dicortazar@gmail.com                 | NULL     | git    | 3ca4e85 |
| 4fcec5a | dpose                          | dpose@sega.bitergia.net              | NULL     | git    | 4fcec5a |
| 5b358fc | dpose                          | dpose@bitergia.com                   | NULL     | git    | 5b358fc |
| 692ad15 | Andre Klapper                  | a9016009@gmx.de                      | NULL     | git    | 692ad15 |
| 6dcf98c | Daniel Izquierdo               | dizquierdo@bitergia.com              | NULL     | git    | 6dcf98c |
| 75fc28e | Santiago Dueñas                | sduenas@bitergia.com                 | NULL     | git    | 75fc28ef |
| 7ad0031 | Alvaro del Castillo            | acs@thelma.cloud                     | NULL     | git    | 7ad0031 |
| 8fac15f | alpgarcia                      | alpgarcia@gmail.com                  | NULL     | git    | 8fac15fd |
| 9aed245 | Alvaro del Castillo            | acs@bitergia.com                     | NULL     | git    | 9aed245 |
...
```

We can observe how all uuids are different, and for eachh row, equal to ids. This is because we have run no merging operation on SortingHat, and for now each unique identity correspond to one identity found in repositories (repo identity). We can see how the source for all the identities is `git` (we only analyzed git repositories). All identities have `name` and `email`, but don't have `username` (it is NULL), since it is not data found in the email addresses found in git repositories. All of these identities were found either as authors of committers of some commit in the analyzed git repositories.

The `uidentities` table just lists the valid unique identities (in this case, I'm showing full hashes):

```bash
mysql -u user -pXXX -e 'SELECT * FROM identities;' shdb
| uuid                                     |
| 0cac4ef12631d5b0ef2fa27ef09729b45d7a68c1 |
| 0ef1c4a95006b07416b0a48ca66587ddfff184e4 |
| 11cc0348b60711cdee515286e394c961388230ab |
| 35c0421704928bcbe3a0d9a4de1d79f9590ccaa9 |
| 37a8187909592a7b78559399105f6b5404af9e4e |
| 3ca4e85833adcf1c6eb7733ba30bf0e9a6956731 |
| 4fcec5a968246d8342e4acfceb9174531c8545c1 |
| 5b358fc11019cf2c03ea4c162009e89715e590dd |
| 692ad158c742a5c8477af1cbd20e37d31cd72aeb |
| 6dcf98c180e858d5643ff48569b152509325b632 |
| 75fc28ef4643de5323e89fb26e4e67c97b24f507 |
| 7ad0031fa2db40a5149f54dfc2ec2a355e9443cd |
| 8fac15fd52da7b984f0b2bbfe1b7ff8f7c93f461 |
| 9aed245d9df109f8d00ca0e656121c3bdde46a2a |
...
```

### The profiles table

The profiles table includes the profiles for all unique identities: the data that is attached by default for each identity, and which can be used to show information about each person in the dashboard. It includes the following fields:

* the  `uuid`
* `name`
* `email`
* `is_bot`
* `country_code`

