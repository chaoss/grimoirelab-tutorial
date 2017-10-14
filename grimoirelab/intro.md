# GrimoireLab architecture

GrimoireLab is a platform for making it easy to apply analytics on data related to software development. It provides components for:

* Automatic and incremental data retrieval from software development support systems (data sources). Those include source code management, issue tracking, communication, testing, code review systems, among others.
* Automatic organziation and enrichment of retrieved data, so that it can be analyzed more easily.
* Management of different identities for the same person, and other data related to persons, such as affiliation to companies.
* Visualization of the data in actionable dashboards.
* Production of reports about specific aspects of software development processes.

Most of the components in GrimoireLab are written in Python, and provide Python APIs and standalone programs.

## Components

The main components of GrimoireLab are:

* Perceval. Includes components for retrieving data from data sources. All components provide an uniform API for accessing their data sources, based on Python generators and data dictionaries (JSON documents).
* Arthur. Organizes the data retrieval from large collections of repositories of different kinds, providing a uniform API to all of them, and to the different retrieval jobs running in any moment.
* GrimoireELK. Collects data retrieved by Arthur, or directly by Perceval, and stores it in ElasticSearch indexes (raw indexes). It also organizes and transforms those raw indexes into other ElasticSearch indexes (enriched indexes), more suitable for visualization or reporting.
* SortingHat. Manages identities for persons, including capabilities for merging the many identities corresponding to the same person, and other data related to them (such as affiliation to companies).
* Kibiter. Visualization platform. It is a soft fork of Kibana, which allows for the construction of actionable dashboards to show the data in enriched indexes.
* Panels. Definition of Kibiter dashboards. They encode the panels, visualizations and other details needed to produce dashboards in Kibiter or Kibana.
* Reports. Production of PDF documents reporting on the main characteristics of a project.
* Mordred. Manages the configuration of all the components needed to produce a dashboard, automating its production.

