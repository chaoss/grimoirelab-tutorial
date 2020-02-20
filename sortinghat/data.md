## SortingHat data structure

SortingHat uses a database to store data about identities.
We will add some more repositories to the index we had produced with
GrimoireELK, and then experiment with the data structures
that SortingHat manages.

### Adding more data to the index

We already [built an index with SortingHat support](../gelk/sortinghat.html),
and produced a dashboard showing it.
But there is still a lot of SortingHat to learn,
if we want to use all of its capacities.
In this chapter we will learn how to use SortingHat in combination to other GrimoireLab tools (mainly Perceval and `p2o.py`). For a more complete guide to SortingHat, read the [SortingHat README](https://github.com/chaoss/grimoirelab-sortinghat/blob/master/README.md).

We will start by adding some more repositories to the index, to have some more complete data. Then we will use it to explore the capabilities of SortingHat for merging identities, for adding affiliations and for adapting profiles.

```bash
(gl) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/GrimoireELK.git
(gl) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/panels.git
(gl) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/mordred.git
(gl) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/arthur.git
(gl) $ p2o.py --enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/training.git
```

When we run `p2o.py` in all these cases, it uses Perceval to retrieve data from the corresponding git repositories, producing a raw index (`git_raw`). Based on it, `p2o.py` later produces the enriched index (`git`). Here is where SortingHat enters the game. Each new identity that `p2o.py` finds while enriching the raw index (in the case of git repositories, usually email addresses and names) is added to SortingHat. When looking in the SortingHat database we will see all these identities. Additionally, with the information stored in SortingHat, `p2o.py` produces some fields in the enriched index, such as the organziation or the name to show in the dashboard for each developer.

Therefore, SortingHat controls how identities are matched to people, and people to organizations. It also controls how people are shown in the indexes. Let's see how.

### Data structure

Before entering into how to use SortingHat,
let's visit the data structure of the database it maintains.
See [A dashboard with SortingHat](../gelk/sortinghat.md), and the introduction to this chapter, for details on how the database was produced; `user` and `XXX` are the credentials to access the `shdb` database. For finding out about its tables, just query MySQL.

```bash
$ mysql -u user -pXXX -e 'SHOW TABLES;' shdb
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

The aim of each table is as follows:

* `identities`: identities found in repositories, and to which unique (merged) identity correspond each of them.
* `uidentities`: unique (merged)) identities.
* `profiles`: information to show in the dashboard for a unique identity.
* `organizations`: organizations to which unique identities may be affiliated.
* `enrollments`: relationship between unique identities and organizations.
* `countries`: countries which can be used in profiles.
* `domains_organizations`: email domains for organizations, used to infer affiliation relationships.
* `matching_blacklist`: identities that should not be merged with others

The `organizations`, `enrollments` and `domain_organziations` tables are empty, because for now, no information about organizations, nor relationship between persons and organizations, has been established. They will be filled when we later take care of that. By the way, this is the reason why in the dashboard up to know all persons appear as affiliated to `Unknown`, which is the label `p2o.py` uses for the organziation when no organization is found for a unique identifier.

Now, let's visit the most important of those, exploring the data we have for them in our database.

### The identities and the uidentities tables

Each identity in the `identity` table is a tuple composed of the following fields:

* a unique identifier (a hash of the other fields, `id`)
* a name (`name`), an email address (`email`)
* a username (`username`)
* the source where the identity was found (`source`, with tags identifying the kind of repository where the identity was found, such as `git`, `bugzilla` or `github`)
* the merged identity to which it corresponds (`uuid`)

All fields in the tuple except for `uuid` a immutable: they never change during the live of a SortingHat database. The `uuid` is used to merge identities that correspond to the same person: each person should have a single `uuid`, and that `uuid` will be in this table for all the identities corresponding to that person. In fact, the `uuid` is the `id` of one of those identities. The name, the email address and the username are the data composing the identity.

For example, email addresses usually have `name` and `email` (such as "Jesus Gonzalez <jgb@bitergia.com>), while `username` is `NULL`. GitHub accounts usually have `name` and `username` (such as "Jesus Gonzalez, jgbarah"), with `email` as `NULL`. The `uuid` will change during the life of the database as new identities for the same person are found, or as wrong merged identities are identified (and broken). A large part of the maintenance of a SortingHat database consists of dealing with `uuid` in the `identities` table, while merging and unmerging identities.

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
| 75fc28e | Santiago Dueñas                | sduenas@bitergia.com                 | NULL     | git    | 75fc28e |
| 7ad0031 | Alvaro del Castillo            | acs@thelma.cloud                     | NULL     | git    | 7ad0031 |
| 8fac15f | alpgarcia                      | alpgarcia@gmail.com                  | NULL     | git    | 8fac15f |
| 9aed245 | Alvaro del Castillo            | acs@bitergia.com                     | NULL     | git    | 9aed245 |
...
```

We can observe how all uuids are different, and for each row, equal to ids. This is because we have run no merging operation on SortingHat, and for now each unique identity corresponds to one identity found in repositories (repo identity). We can see how the source for all the identities is `git` (we only analyzed git repositories). All identities have `name` and `email`, but don't have `username` (it is NULL), since it is not data found in the email addresses found in git repositories. All of these identities were found either as authors of committers of some commit in the analyzed git repositories.

The `uidentities` table just lists the valid unique identities (in this case, I'm showing full hashes):

```bash
mysql -u user -pXXX -e 'SELECT * FROM uidentities;' shdb
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

* the unique identifier for the profile, `uuid`
* the name, `name`
* the email address `email`
* a boolean labeling the identity as a bot, `is_bot`
* a country code, `country_code`

For example, in our case:

```bash
mysql -u user -pXXX -e 'SELECT * FROM profiles;' shdb
| uuid    | name                           | email                                | is_bot | country_code |
| 0cac4ef | Quan Zhou                      | quan@bitergia.com                    |      0 | NULL         |
| 0ef1c4a | Jesus M. Gonzalez-Barahona     | jgbarah@gmail.com                    |      0 | NULL         |
| 11cc034 | quan                           | zhquan7@gmail.com                    |      0 | NULL         |
| 35c0421 | Alberto Martín                 | alberto.martin@bitergia.com          |      0 | NULL         |
| 37a8187 | Alberto Martín                 | albertinisg@users.noreply.github.com |      0 | NULL         |
| 3ca4e85 | Daniel Izquierdo Cortazar      | dicortazar@gmail.com                 |      0 | NULL         |
| 4fcec5a | dpose                          | dpose@sega.bitergia.net              |      0 | NULL         |
| 5b358fc | dpose                          | dpose@bitergia.com                   |      0 | NULL         |
| 692ad15 | Andre Klapper                  | a9016009@gmx.de                      |      0 | NULL         |
| 6dcf98c | Daniel Izquierdo               | dizquierdo@bitergia.com              |      0 | NULL         |
| 75fc28e | Santiago Dueñas                | sduenas@bitergia.com                 |      0 | NULL         |
| 7ad0031 | Alvaro del Castillo            | acs@thelma.cloud                     |      0 | NULL         |
| 8fac15f | alpgarcia                      | alpgarcia@gmail.com                  |      0 | NULL         |
| 9aed245 | Alvaro del Castillo            | acs@bitergia.com                     |      0 | NULL         |
...
```

All `is_bot` are 0 because that's the default value (false), and we have not specifically labeled any unique identifier as bot. All `country_code` are `NULL` because we have not identified countries in any way. For the rest of the fields, you may notice how SortingHat just used the information it had from the repo identities.

When we unify repo identities (merging several into a single unique identity), we usually need to check the corresponding entry in this table, for ensuring the profile information is correct.

### Enrollments and organizations

Up to now we have not used SortingHat to assign organizations to persons (unique identities). Therefore, `enrollments` and `organizations` tables are empty. But we can check their structure.

```
$ mysql -u user -pXXX -e 'DESCRIBE organizations;' shdb
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int(11)      | NO   | PRI | NULL    | auto_increment |
| name  | varchar(255) | NO   | UNI | NULL    |                |
+-------+--------------+------+-----+---------+----------------+

``` 

In this format, each row corresponds to the description of a field in the `organizations` table. We can see how simple it is: just an identifier (for linking with other tables) and a name for each organization.

`enrollments` table is a bit more complex:

```
$ mysql -u user -pXXX -e 'DESCRIBE enrollments;' shdb
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| id              | int(11)      | NO   | PRI | NULL    | auto_increment |
| start           | datetime     | NO   |     | NULL    |                |
| end             | datetime     | NO   |     | NULL    |                |
| uuid            | varchar(128) | NO   | MUL | NULL    |                |
| organization_id | int(11)      | NO   | MUL | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
```

This table stores the "periods of enrollment": relationships between persons (unique identities) and organizations, which happen during a certain period of time (from `start` to `end`). You can read each row in this table as "the person with this `uuid` worked for the organization `organization_id` during this period.
