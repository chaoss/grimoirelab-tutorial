# Retrieving Code Complexity via CoCom Backend

- [CoCom](https://github.com/chaoss/grimoirelab-graal/blob/master/graal/backends/core/cocom.py) ( Code Complexity ) Backend based on supported languages and with the help of [Lizard](https://github.com/terryyin/lizard) retrieves various source code related analysis such as:
  - Cyclomatic Complexity and Average Cyclomatic Complexity
  - Lines of Code and Average Lines of Code
  - Number of functions in a module
  - Total number of tokens
  - ( and many more )

## Basic usage of the CoCom backend

Once you've successfully installed Graal, you can get started real quick with the command line interface as easy as -

```sh
(graal) $ graal cocom --help
```

**Note:** You can invoke other available backends in a similar way.

## Using Graal as a program

- Let's start our analysis with the host repository itself. As you can see the positional parameter is added with the repository url and `git-path` flag is used to define the path where the git repository will be cloned.

```sh
(graal) $ graal cocom https://github.com/chaoss/grimoirelab-graal --git-path /tmp/graal-cocom
[2019-03-27 21:32:03,719] - Starting the quest for the Graal.
[2019-03-27 21:32:11,663] - Git worktree /tmp/worktrees/graal-cocom created!
[2019-03-27 21:32:11,663] - Fetching commits: 'https://github.com/chaoss/grimoirelab-graal' git repository from 1970-01-01 00:00:00+00:00 to 2100-01-01 00:00:00+00:00; all branches
[2019-03-27 21:32:13,276] - Git repository /tmp/graal-cocom checked out!
...
{
    "backend_name": "CoCom",
    "backend_version": "0.2.3",
    "category": "code_complexity",
    "data": {
        "Author": "Valerio Cosentino <valcos@bitergia.com>",
        "AuthorDate": "Sun May 6 13:56:51 2018 +0200",
        "Commit": "Valerio Cosentino <valcos@bitergia.com>",
        "CommitDate": "Sun May 6 13:56:51 2018 +0200",
        "analysis": [
            {
                "avg_ccn": 2.111111111111111,
                "avg_loc": 9.11111111111111,
                "avg_tokens": 64.0,
                "blanks": 48,
                "ccn": 19,
                "comments": 63,
                "ext": "py",
                "file_path": "graal/codecomplexity.py",
                "loc": 129,
                "num_funs": 9,
                "tokens": 786
            }
        ],
        "commit": "a957488c9bd95e3b72a30611edc61496ee152430",
        "message": "[codecomplexity] Enable analysis with no file filtering\n\nThis patch allows to handle analysis without file filtering."
    },
    "graal_version": "0.1.0",
    "origin": "https://github.com/chaoss/grimoirelab-graal",
    "tag": "https://github.com/chaoss/grimoirelab-graal",
    "timestamp": 1553702540.824002,
    "updated_on": 1525607811.0,
    "uuid": "ce7c47568fd87100aff497dd7677b0736d85db1e"
}
...
[2019-03-27 21:35:59,077] - Fetch process completed: 137 commits fetched
[2019-03-27 21:35:59,089] - /tmp/worktrees/graal-cocom deleted!
[2019-03-27 21:35:59,116] - Git worktree /tmp/worktrees/graal-cocom deleted!
[2019-03-27 21:35:59,116] - Fetch process completed: 137 commits inspected
[2019-03-27 21:35:59,117] - Quest completed.
```

- In the above graal output, you can read one commit item obtained which contains "analysis" attribute under "data".

**Note:** Some of the intermediate output items are skipped for representational purposes.

## Using Graal as a Python script

- We can also use the backend provided by Graal in python scripts via importing the appropriate modules. Show below is using `cocom` backend in a python script. [ Example: [graal_cocom_1.py](./scripts/graal_cocom_1.py) ]

```python3
#! /usr/bin/env python3
from graal.backends.core.cocom import CoCom

# URL for the git repo to analyze
repo_uri = "http://github.com/chaoss/grimoirelab-graal"

# directory where to mirror the repo
repo_dir = "/tmp/graal-cocom"

# Cocom object initialization
cc = CoCom(uri=repo_uri, git_path=repo_dir)

# fetch all commits
commits = [commit for commit in cc.fetch()]
```

- The above `commits` list contains commit items and can be used for further extraction of specific attributes.
