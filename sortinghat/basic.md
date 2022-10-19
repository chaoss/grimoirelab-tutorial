

## Basic use

In the previous section we saw a part of the `identities` table, which stores the repo identities found, and their relationship with unique identities (`uuid`):

| id      | name                           | email                                | username | source | uuid    |
|---------|--------------------------------|--------------------------------------|----------|--------|---------|
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

### Merging identities

It is obvious that there are some repo identities in it that correspond to the same person. In SortingHat, that means they should point to the same unique identity (`uuid`). But that is not the case, because in fact we have never told SortingHat they correspond to the same person. That operation is called "merging".

For example, let's merge repo identity `4fcec5a` (dpose, dpose@sega.bitergia.net) with `5b358fc` (dpose, dpose@bitergia.com), which I know correspond to the same person:

 ```bash
 (gl) $ sortinghat -u user -p XXX -d shdb merge \
   4fcec5a968246d8342e4acfceb9174531c8545c1 5b358fc11019cf2c03ea4c162009e89715e590dd
 Unique identity 4fcec5a968246d8342e4acfceb9174531c8545c1 merged on 5b358fc11019cf2c03ea4c162009e89715e590dd
 ```

Notice that we had to use the complete hashes (in the table above, and in the listing in the previous section, we shortened them just for readability). What we have done is to merge `4fcec5a` on `5b358fc`, and the result is:

```bash
mysql -u user -pXXX -e 'SELECT * FROM identities WHERE uuid LIKE "5b358fc%";' shdb
| id      | name  | email                   | username | source | uuid    |                                 
| 4fcec5a | dpose | dpose@sega.bitergia.net | NULL     | git    | 5b358fc |
| 5b358fc | dpose | dpose@bitergia.com      | NULL     | git    | 5b358fc |
```

The query looked for all rows in the `identities` table whose `uuid` field starts with `5b358fc`, and found two: the repo identifier `5b358fc`, which was already linked to it, but also `4fcec5a`, which we just merged onto it. This way we have learnt that when we merge, we merge a repo identity (the first argument) on a unique identity (the second argument).

We can follow this procedure for other identities that correspond to the same person: (Quan Zhou, quan@bitergia.com) and (quan, zhquan7@gmail.com); (Alberto Martín, alberto.martin@bitergia.com) and (Alberto Martín, albertinisg@users.noreply.github.com); and (Alvaro del Castillo, acs@thelma.cloud) and (Alvaro del Castillo, acs@bitergia.com):

```bash
(gl) $ sortinghat -u user -p XXX -d shdb merge \
  0cac4ef12631d5b0ef2fa27ef09729b45d7a68c1 11cc0348b60711cdee515286e394c961388230ab
Unique identity 0cac4ef12631d5b0ef2fa27ef09729b45d7a68c1 merged on 11cc0348b60711cdee515286e394c961388230ab
(gl) $ sortinghat -u user -p XXX -d shdb merge \
  35c0421704928bcbe3a0d9a4de1d79f9590ccaa9 37a8187909592a7b78559399105f6b5404af9e4e
Unique identity 35c0421704928bcbe3a0d9a4de1d79f9590ccaa9 merged on 37a8187909592a7b78559399105f6b5404af9e4e
(gl) $ sortinghat -u user -p XXX -d shdb merge \
  7ad0031fa2db40a5149f54dfc2ec2a355e9443cd 9aed245d9df109f8d00ca0e656121c3bdde46a2a
Unique identity 7ad0031fa2db40a5149f54dfc2ec2a355e9443cd merged on 9aed245d9df109f8d00ca0e656121c3bdde46a2a
```

### Showing information about a unique identity

Now, we can check how SortingHat is storing information about these merged identities, but instead of querying directly the database, we can just use `sortinghat`:

```bash
(gl) $ sortinghat -u user -p XXX -d shdb show \
  11cc0348b60711cdee515286e394c961388230ab
unique identity 11cc0348b60711cdee515286e394c961388230ab

Profile:
    * Name: quan
    * E-Mail: zhquan7@gmail.com
    * Bot: No
    * Country: -

Identities:
  0cac4ef12631d5b0ef2fa27ef09729b45d7a68c1	Quan Zhou	quan@bitergia.com	-	git
  11cc0348b60711cdee515286e394c961388230ab	quan	zhquan7@gmail.com	-	git

No enrollments
```

That is, we have two repo identities for this person, which we're identifying in the profile as `quan`, with email address `zhquan7@gmail.com`. Remember that the profile was already produced when each repo identity was added to the database, by creating a unique identity for it, and using the data in the repo identity for the profile.

We merged the repo identity (Quan Zhou, quan@bitergia.com) on the unique identity that corresponded to (quan, zhquan7@gmail.com), which had as profile (quan, zhquan7@gmail.com) as well. Therefore, the unique identity after the merge conserves the old profile, in this case (quan, zhquan7@gmail.com). Should we have merged the other way around, we would have considered (Quan Zhou, quan@bitergia.com) as the profile, which in this case seems more convenient. So, we have to be careful about how to merge, if we want to conserve the most interesting profiles.

Unfortunately, we cannot redo the merge with the most convenient order:

```bash
(gl) $ sortinghat -u user -p XXX -d shdb merge \
  11cc0348b60711cdee515286e394c961388230ab 0cac4ef12631d5b0ef2fa27ef09729b45d7a68c1
Error: 0cac4ef12631d5b0ef2fa27ef09729b45d7a68c1 not found in the registry
```

Why? Because `0cac4ef` is no longer a valid unique identifier: we lost it when we merged the repo identity `0cac4ef`, which was the only one pointing to it. So, we cannot merge any repo identifier on it, since it no longer exists.

Later on we will revisit this case, since there are stuff that can be done: breaking the unique identifier into two. But for now, let's use another approach to solve this problem.

### Modifying profiles

We can just modify the profile for the unique identity, thus changing the profile for a person:

```bash
(gl) $ sortinghat -u user -p XXX -d shdb profile \
  --name "Quan Zhou" --email "quan@bitergia.com" \
  11cc0348b60711cdee515286e394c961388230ab
unique identity 11cc0348b60711cdee515286e394c961388230ab

Profile:
    * Name: Quan Zhou
    * E-Mail: quan@bitergia.com
    * Bot: No
    * Country: -
```

This way we have the name and email address we want. Using `--country` we can also set a country for the person.

### Regenerating enriched indexes

When we interact with SortingHat, it only changes the contents of the database it manages. Therefore, the changes are not reflected in the indexes we have in ElasticSearch, nor in the dashboard.

To make changes appear in the dashboard, we need to create new enriched indexes (re-enrich the indexes). We can do that by removing raw and enriched indexes from ElasticsSearch, and then running the same `p2o.py` commands shown to produce new raw and enriched indexes. But in our case, this is a clear overkill: we don't need to retrieve new raw indexes from the repositories, since they are fine. We only need to produce new enriched indexes. For that, we can run `p2o.py` as follows:

```
(gl) $ p2o.py --only-enrich --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/GrimoireELK.git
```

I only used the `--only-enrich` option, instead of `--enrich`. This option will not try to retrieve data from the data sources, and then enrich it. It will just use the specified raw index to create the enriched one.

In this case, the command will create a new `git` index (by modifying the current one) for items (commits) from the specified repository (`GrimoireELK`). We need to run this command for all the repositories with identities affected by the changes. Once we have those new indexes, we're done: the changes will be reflected in the dashboard.

### Regenerating enriched indexes (take two)

The above method, even when it will work, is still an overkill. I really don't need to modify the whole enriched indexes, by updating all the fields in their items. We just need to update the fields related to identities, which are the only ones that we need to change. For that, we have a specific option to `p2o.py`:

```
(gl) $ p2o.py --only-enrich --refresh-identities --index git_raw --index-enrich git \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/GrimoireELK.git
```

In addition to the `--only-enrich` option, which was explained above, I have added the `--refresh-identities`, which ensures that only identities, and not all fields in each item, are updated. And this was exactly what we needed. We still need to run the command for all the repositories affected, but that's all.

### Regenerating enriched indexes (take three)

In most cases, when the SortingHat database is modified, only a handful of identities are changed. That means that we don't really need to change all the identities in enriched indexes. We can avoid this time-consuming operation (when the indexes are large) by changing only the items affected: those with changed identities.

In this case, the command to run is:

```
(gl) $ p2o.py --only-enrich --refresh-identities --index git_raw --index-enrich git \
  --author_uuid 11cc0348b60711cdee515286e394c961388230ab \
    0cac4ef12631d5b0ef2fa27ef09729b45d7a68c1 \
  -e http://localhost:9200 --no_inc --debug \
  --db-host localhost --db-sortinghat shdb --db-user user --db-password XXX \
  git https://github.com/grimoirelab/GrimoireELK.git
```

The magic is done by the `--author_uuid` option, which will ensure that only items with that `author_uuid` field are refreshed. In this case, we're refreshing them for unique identities `11cc034` and `0cac4ef`, which were changed in the SortingHat database in the process above. Again, this should be done for all the repositories affected.

Something similar can be done with the `--author_id`, but in this case for repo identities of the author.
