---
layout: default
title: Setup.cfg
nav_order: 1
parent: Configure GrimoireLab
grand_parent: Getting-started
---

# Setup.cfg

The setup file holds the configuration to arrange all process underlying
GrimoireLab. It is composed of sections which allow to define the general
settings such as which phases to activate (e.g., collection, enrichment) and
where to store the logs, as well as the location and credentials for SortingHat
and the ElasticSearch instances where the raw and enriched data is stored.
Furthermore, it also includes backend sections to set up the parameters used by
Perceval to access the software development tools (e.g., GitHub tokens, gerrit
username) and fetch their data.

Dashboards can be automatically uploaded via the `setup.cfg` if the phase
`panels` is enabled. The `Data Status` and `Overview` dashboards will contain
widgets that summarize the information of the data sources declared in the
`setup.cfg`. Note that the widgets are not updated when adding new data sources,
thus you need to manually delete the dashboards `Data Status` and `Overview`,
and restart mordred again (making sure that the option `panels` is enabled).

### [es_collection]

- **url** (str: http://172.17.0.1:9200): Elasticsearch URL (**Required**)

### [es_enrichment]

- **autorefresh** (bool: true): Execute the autorefresh of identities
- **autorefresh_interval** (int: 2): Time interval (days) to autorefresh
  identities
- **url** (str: http://172.17.0.1:9200): Elasticsearch URL (**Required**)

### [general]

- **bulk_size** (int: 1000): Number of items to write in Elasticsearch using
  bulk operations
- **debug** (bool: true): Debug mode (logging mainly) (**Required**)
- **logs_dir** (str: logs): Directory with the logs of sirmordred (**Required**)
- **min_update_delay** (int: 60): Short delay between tasks (collect, enrich
  ...)
- **scroll_size** (int: 100): Number of items to read from Elasticsearch when
  scrolling
- **short_name** (str: Short name): Short name of the project (**Required**)
- **update** (bool: false): Execute the tasks in loop (**Required**)
- **aliases_file** (str: ./aliases.json): JSON file to define aliases for raw
  and enriched indexes
- **menu_file** (str: ./menu.yaml): YAML file to define the menus to be shown in
  Kibiter
- **global_data_sources** (list: bugzilla, bugzillarest, confluence, discourse,
  gerrit, jenkins, jira): List of data sources collected globally, they are
  declared in the section 'unknown' of the projects.json
- **retention_time** (int: None): the maximum number of minutes wrt the current
  date to retain the data

### [panels]

- **community** (bool: true): Include community section in dashboard
- **kibiter_default_index** (str: git): Default index pattern for Kibiter
- **kibiter_time_from** (str: now-90d): Default time interval for Kibiter
- **kibiter_url** (str): Kibiter URL (**Required**)
- **kibiter_version** (str: None): Kibiter version
- **kafka** (bool: false): Include KIP section in dashboard
- **github-comments** (bool: false): Enable GitHub comments menu. Note that if
  enabled, the github2:issue and github2:pull sections in the setup.cfg and
  projects.json should be declared
- **github-events** (bool: false): Enable GitHub events menu. Note that if
  enabled, the github:event section in the setup.cfg and projects.json should be
  declared
- **github-repos** (bool: false): Enable GitHub repo stats menu. Note that if
  enabled, the github:repo section in the setup.cfg and projects.json should be
  declared
- **gitlab-issues** (bool: false): Enable GitLab issues menu. Note that if
  enabled, the gitlab:issue section in the setup.cfg and projects.json should be
  declared
- **gitlab-merges** (bool: false): Enable GitLab merge requests menu. Note that
  if enabled, the gitlab:merge sections in the setup.cfg and projects.json
  should be declared
- **mattermost** (bool: false): Enable Mattermost menu
- **code-license** (bool: false): Enable code license menu. Note that if
  enabled, colic sections in the setup.cfg and projects.json should be declared
- **code-complexity** (bool: false): Enable code complexity menu. Note that if
  enabled, cocom sections in the setup.cfg and projects.json should be declared
- **strict** (bool: true): Enable strict panels loading
- **contact** (str: None): Support repository URL

### [phases]

- **collection** (bool: true): Activate collection of items (**Required**)
- **enrichment** (bool: true): Activate enrichment of items (**Required**)
- **identities** (bool: true): Do the identities tasks (**Required**)
- **panels** (bool: true): Load panels, create alias and other tasks related
  (**Required**)

### [projects]

- **projects_file** (str: projects.json): Projects file path with repositories
  to be collected grouped by projects
- **projects_url** (str: None): Projects file URL, the projects_file is required
  to store the file locally

### [sortinghat]

- **affiliate** (bool: true): Affiliate identities to organizations
  (**Required**)
- **autogender** (bool: false): Add gender to the profiles (executes autogender)
- **autoprofile** (list: ['customer', 'git', 'github']): Order in which to get
  the identities information for filling the profile (**Required**)
- **database** (str: sortinghat_db): Name of the Sortinghat database
  (**Required**)
- **host** (str: mariadb): Host with the Sortinghat database (**Required**)
- **identities_api_token** (str: None): API token for remote operation with
  GitHub and Gitlab
- **identities_export_url** (str: None): URL in which to export the identities
  in Sortinghat
- **identities_file** (list: []): File path with the identities to be loaded in
  Sortinghat
- **identities_format** (str: sortinghat): Format of the identities data to be
  loaded
- **load_orgs** (bool: false):
- **matching** (list: ['email']): Algorithm for matching identities in
  Sortinghat (**Required**)
- **orgs_file** (str: None): File path with the organizations to be loaded in
  Sortinghat
- **password** (str: ): Password to access the Sortinghat database
  (**Required**)
- **reset_on_load** (bool: false): Unmerge and remove affiliations for all
  identities on load
- **sleep_for** (int: 3600): Delay between task identities executions
  (**Required**)
- **strict_mapping** (bool: true): rigorous check of values in identities
  matching (i.e, well formed email addresses, non-overlapping enrollment
  periods)
- **unaffiliated_group** (str: Unknown): Name of the organization for
  unaffiliated identities (**Required**)
- **user** (str: root): User to access the Sortinghat database (**Required**)

### [backend-name:tag] (tag is optional)

- **collect** (bool: true): enable/disable collection phase
- **raw_index** (str: None): Index name in which to store the raw items
  (**Required**)
- **enriched_index** (str: None): Index name in which to store the enriched
  items (**Required**)
- **studies** (list: []): List of studies to be executed
- **anonymize** (bool: false): enable/disable anonymization of personal user
  information
- **backend-param-1**: ..
- **backend-param-2**: ..
- **backend-param-n**: ..

The template of a backend section is shown above. Further information about
Perceval backends parameters are available at:

- Params details:
  http://perceval.readthedocs.io/en/latest/perceval.backends.core.html
- Examples:
  https://github.com/chaoss/grimoirelab-sirmordred/blob/master/tests/test_studies.cfg

Note that some backend sections allow to specify specific enrichment options,
which are listed below.

### [jenkins]

- **node_regex**: regular expression for extracting node name from `builtOn`
  field. This regular expression **must contain at least one group**. First
  group will be used to extract node name. More groups are allowed but not used
  to extract anything else.

### [studies-name:tag] (tag is optional)

- **study-param-1**: ..
- **study-param-2**: ..
- **study-param-n**: ..