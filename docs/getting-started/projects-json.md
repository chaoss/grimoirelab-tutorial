---
layout: default
title: projects.json
nav_order: 1
parent: Configure GrimoireLab
grand_parent: Getting Started
---

# projects.json

The `projects.json` aims at describing the repositories grouped by project that
will be shown on the dashboards.

The project file enables the users to list the instances of the software
development tools to analyse, such as local and remote Git repositories, the
URLs of GitHub and GitLab issue trackers and the name of Slack channels.
Furthermore, it also allows the users to organize these instances into nested
groups, which structure is reflected in the visualization artifacts (i.e.,
documents and dashboards). Groups can be useful to represent projects within a
single company, sub-projects within a large project such as Linux and Eclipse,
or the organizations within a collaborative project.

1. **First level**: project names
2. **Second level**: data source and metadata
3. **Third level**: data source URLs

There are some filters, labels, and a special section:

- `--filter-no-collection=true`: This filter is used to show old enriched data
  within the dashboards from repositories that don't exist anymore in upstream.
- `--filter-raw` and the section `unknown`: The data sources will only be
  collected at the section `unknown` but this allows user to add the same data
  source in different sections to enrich using the filter `--filter-raw`.
- Label ` --labels=[example]`: The data source will have the label of `example`
  which can be used to create visualisations for specific sets of data
- Section `unknown`: If the data source is only under this section it will be
  enriched as project `main`.

```
{
   "Chaoss":{
      "gerrit":[
         "gerrit.chaoss.org --filter-raw=data.projects:CHAOSS"
      ],
      "git":[
         "https:/github.com/chaoss/grimoirelab-perceval",
         "https:/github.com/chaoss/grimoirelab-sirmordred"
      ],
      "github":[
         "https:/github.com/chaoss/grimoirelab-perceval --filter-no-collection=true",
         "https:/github.com/chaoss/grimoirelab-sirmordred  --labels=[example]"
      ]
   },
   "GrimoireLab":{
      "gerrit":[
         "gerrit.chaoss.org --filter-raw=data.projects:GrimoireLab"
      ]
   },
   "unknown":{
      "gerrit":[
         "gerrit.chaoss.org"
      ],
      "confluence":[
         "https://wiki.chaoss.org"
      ]
   }
}
```

In the `projects.json` above:

- The data included in the repo `gerrit.chaoss.org` will be collected entirely
  since the repo is listed in the `unknown` section. However only the project
  `GrimoireLab` will be enriched as declared in the `GrimoireLab` section.
- In the section `Chaoss` in the data source `github` the repository
  `grimoirelab-perceval` is not collected for raw index but it will enriched in
  the enriched index.
- In the section `GrimoireLab` the metadata will showed in the enriched index as
  extra fields.
- In the section `unknown` the data source `confluence` will be enriched as the
  project `main`.
