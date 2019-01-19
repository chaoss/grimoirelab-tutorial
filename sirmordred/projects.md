## The projects file

An important part of the information provided to Mordred is the list of projects to analyze, and how they are structured in repositories. This is done in the projects file.

The projects file is a JSON file with the following structure:

```
{
    "Project1": {
        "datasource1": [ list_of_repos_11 ],
        "datasource2": [ list_of_repos_12 ],
        ...
        "datasourcen": [ list_of_repos_1n ]
    },
    "Project2": {
        ...
    },
    ...
    "Projectk": {
    }
}
```

That is, in Python terms it is a dictionary of projects, where the key for each project is the project name (as we want it to appear in the dashboard), and the value is a dictionary with the data sources for that project.

In turn the dictionary with data sources has as keys the Perceval identifiers for the data sources of interest for the project (for example "git", "github", "jira", etc.). Values of that dictionary is a list of repositories, also in the format expected by Perceval. See `perceval --help`, or the [main Perceval README](https://github.com/chaoss/grimoirelab-perceval/blob/master/README.md) for a complete list of data sources supported, and their identifiers. For convenience, this is a close-to-complete list:

* askbot: Questions and answers from Askbot site
* bugzilla: Bugzilla server
* bugzillarest: Bugzilla server (>=5.0) using its REST API
* confluence: Confluence server
* discourse: Discourse site
* gerrit: Gerrit server
* git: Commits from Git
* github: Issues and PRs from GitHub
* gmane: Gmane messages (not working now)
* hyperkitty: Messages from a HyperKitty archiver
* jenkins: Builds data from a Jenkins server
* jira: Issues data from JIRA issue tracker
* mbox: Messages from MBox files
* mediawiki: Pages and revisions from a MediaWiki site
* meetup: Events from a Meetup group
* nntp: Articles from a NNTP news group
* phabricator: Tasks from a Phabricator site
* pipermail: Messages from a Pipermail archiver
* redmine: Issues data from a Redmine server
* rss: Entries from a RSS feed server
* slack: Messages from a Slack channel
* stackexchange: Questions, answers and comments from StackExchange sites
* supybot: Messages from Supybot log files
* telegram: Messages from the Telegram server

As an example, this is an excerpt of the projects file for the CHAOSS dashboard:

```
{
    "GrimoireLab": {
        "git": [
            "https://github.com/grimoirelab/arthur",
            "https://github.com/grimoirelab/grimoireelk",
            "https://github.com/grimoirelab/mordred",
            ...
        ],
        "github": [
            "https://github.com/grimoirelab/arthur",
            "https://github.com/grimoirelab/grimoireelk",
            "https://github.com/grimoirelab/mordred",
            ...
        ],
        "pipermail": [
            "https://lists.linuxfoundation.org/pipermail/grimoirelab-discussions"
        ]
    },
    "GHData": {
        "git": [
            "https://github.com/OSSHealth/ghdata"
        ],
        "github": [
            "https://github.com/OSSHealth/ghdata"
        ]
    },
    ...
}
```

Note that for GitHub repos, we need entries both for "git" and "github", since two different Perceval backends are used: the first one for the git repository, the second one for GitHub issues and pull requests.

Once we have completed the file, we have to specify its name in the `mordred.cfg` file (section "projects", parameter "projects_file"). For example, if the file is `/home/user/projects.json`, the lines in `mordred.cfg` would be:

```
[projects]
projects_file = /home/user/projects.json
```
