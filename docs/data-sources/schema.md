---
layout: default
title: Schema
nav_order: 4
parent: Data Sources
---

# Schema

Every supported data source has a data model that is used for the indexes and
panels in GrimoireLab. The fields described in each data model are the fields
that are expected from ElasticSearch after the enrichment process.

You can check out the data models of the supported data sources
[chaoss/grimoirelab-elk -
schema](https://github.com/chaoss/grimoirelab-elk/tree/master/schema). Each CSV
file will have minimum two columns, name and type.

| name | type |

`name` refers to the actual field. Eg `author_name`, `grimoire_creation_date`

`type` refers to the category of the field. Eg `boolean`, `long`

Some CSV file might have four columns, name, type, aggregatable and description.

| name | type | aggregatable | description |

`aggregatable` refers to whether the field can be aggregated.

`description` gives a brief about the field.
