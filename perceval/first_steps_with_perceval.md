# First steps with Perceval

[Perceval](https://github.com/grimoirelab/perceval) is a Python module for retrieving data from repositories related to software development. It works with many data sources, from git repositories and GitHub projects to mailing lists, Gerrit or StackOverflow, In this section, you will learn the basics of working with it.

## Preparing a virtualenv

I'm assuming you already have Python3 installed (Perceval is written for Python3). Let's start by creating a Python virtual environment, so that we have a cozy place to work. In the following, we will use [Python3's pyvenv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) (available in Debian or Ubuntu as the `python3-venv` package). But using the more traditional [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) should be possible as well.

First, let's create our new environment. I like my Python virtual environments under the `venvs` subdirectory in my home directory, and in this case I will call it `perceval` (see how original I am!):

```bash
$ pyvenv ~/venvs/perceval
```

## Installing Perceval

Once created, you can  activate it (remember it will stay activated only in the shell where you actyvated it). Once activated, install Perceval, which will therefore be present only in your virtual environment. For installing Perceval, we will use pip, which will install it from the [Pypi archive](https://pypi.python.org/pypi).

```bash
$ source ~/venvs/perceval/bin/activate
(perceval) $ pip3 install perceval
```

This will install Perceval and its dependencies (other Python modules that are needed by Perceval to work). So, we're ready to see what it can do.

## Checking that it is installed

For a starter, you can use the `perceval` script, which has been installed in your virtual envirioment, since it comes with the Perceval package. It is a simple front-end to the Perceval module, which gets data from a data source, and writes what it finds as JSON documents in stdout. To learn about its command line arguments, just use the `--help` flag:

```bash
(perceval) $ perceval --help
```

This should produce a banner with information about command line arguments, and a listing of Perceval backends. If that banner doesn't show up, it is likely that something wrong happened during the installation.

Assuming everything was fine, next thing is getting information about an specific backend. Let's start with the git backend, which will be a good starter for testing:

```
(perceval) $ perceval git --help
```

Now that we have Perceval installed, let's give it a try. For that, we will use the git repository for the Perceval source code as the data source to retrieve (do you appreciate the nice recursion here?)

## Using Perceval as a program

To begin with, let's use the `perceval` command that we checked just a moment ago.

```bash
(perceval) $ perceval git https://github.com/grimoirelab/perceval.git
[2016-10-03 00:47:46,632] - Sir Perceval is on his quest.
[2016-10-03 00:47:46,633] - Fetching commits: 'https://github.com/grimoirelab/perceval.git' git repository from 1970-01-01 00:00:00+00:00; all branches
{
    "backend_name": "Git",
    "backend_version": "0.3.0",
    "data": {
        "Author": "Santiago Due\u00f1as <sduenas@bitergia.com>",
        "AuthorDate": "Tue Aug 18 18:08:27 2015 +0200",
        "Commit": "Santiago Due\u00f1as <sduenas@bitergia.com>",
        "CommitDate": "Tue Aug 18 18:08:27 2015 +0200",
        "commit": "dc78c254e464ff334892e0448a23e4cfbfc637a3",
        "files": [
            {
                "action": "A",
                "added": "10",
                "file": ".gitignore",
                "indexes": [
                    "0000000...",
                    "ceaedd5..."
                ],
                "modes": [
                    "000000",
                    "100644"
                ],
                "removed": "0"
            },
            {
                "action": "A",
                "added": "1",
                "file": "AUTHORS",
                "indexes": [
                    "0000000...",
                    "a67f214..."
                ],
                "modes": [
                    "000000",
                    "100644"
                ],
                "removed": "0"
            },
            {
                "action": "A",
                "added": "674",
                "file": "LICENSE",
                "indexes": [
                    "0000000...",
                    "94a9ed0..."
                ],
                "modes": [
                    "000000",
                    "100644"
                ],
                "removed": "0"
            }
        ],
        "message": "Initial import",
        "parents": [],
        "refs": []
    },
    "origin": "https://github.com/grimoirelab/perceval.git",
    "perceval_version": "0.3.0",
    "timestamp": 1475448330.809561,
    "updated_on": 1439914107.0,
    "uuid": "29ddd736146e278feb5d84e9dcc1fd310ff50007"
}
...
[2016-10-03 00:47:47,861] - Fetch process completed: 356 commits fetched
[2016-10-03 00:47:47,862] - Sir Perceval completed his quest.
```

Your output will vary depending on the exact version of Perceval you have, and when you run it. But you will get something similar to this start (with the first commit in Perceval), followed by many more commits, and the final messages. In addition, by redirecting stdout you can notice that JSON documents are actually written to stdout, while progress messages are written in stderr. This makes it easy to get a file with all commits (one JSON document per commit), or to pipe them to some other command. For example:

```bash
(perceval) $ perceval git https://github.com/grimoirelab/perceval.git > /tmp/perceval.test
[2016-10-03 00:53:59,235] - Sir Perceval is on his quest.
[2016-10-03 00:53:59,236] - Fetching commits: 'https://github.com/grimoirelab/perceval.git' git repository from 1970-01-01 00:00:00+00:00; all branches
[2016-10-03 00:54:00,349] - Fetch process completed: 356 commits fetched
[2016-10-03 00:54:00,349] - Sir Perceval completed his quest.
```

This will produce the file `/tmp/perceval.test` with all the retrieved commits.

To produce this result, Perceval cloned the git repository to analyze, and got information for all its commits by using the `git log` commmand under the hoods. Therefore, you need to have git installed, but if you're are in the bussiness of developing software, it would be weird you didn't have.

One interesting detail of this behavior is that Perceval is clonning the git repository once and again, to analyze it. You can tell Perceval where to store it, and reuse it the next time. You will probably notice the difference if you use the time command:

```bash
(perceval) $ time perceval git https://github.com/grimoirelab/perceval.git \
  --git-path /tmp/perceval.git > /tmp/perceval.test
[2016-10-03 01:01:55,360] - Sir Perceval is on his quest.
[2016-10-03 01:01:55,361] - Fetching commits: 'https://github.com/grimoirelab/perceval.git' git repository from 1970-01-01 00:00:00+00:00; all branches
[2016-10-03 01:01:58,195] - Fetch process completed: 356 commits fetched
[2016-10-03 01:01:58,195] - Sir Perceval completed his quest.

real	0m2.991s
user	0m0.544s
sys	0m0.100s

(perceval) $ time perceval git https://github.com/grimoirelab/perceval.git \
  --git-path /tmp/perceval.git > /tmp/perceval.test
[2016-10-03 01:02:00,319] - Sir Perceval is on his quest.
[2016-10-03 01:02:00,321] - Fetching commits: 'https://github.com/grimoirelab/perceval.git' git repository from 1970-01-01 00:00:00+00:00; all branches
[2016-10-03 01:02:01,323] - Fetch process completed: 356 commits fetched
[2016-10-03 01:02:01,323] - Sir Perceval completed his quest.

real	0m1.151s
user	0m0.432s
sys	0m0.032s
```

Of course, differences will be longer for larger repositories.

## Using Perceval as a Python module

But we know that Perceval is a Python library. So, let's use it as a Python library, from a Python script ([perceval_git_1.py](https://github.com/jgbarah/grimoirelab-training/blob/master/perceval/scripts/perceval_git_1.py)):

```python
#! /usr/bin/env python3

import perceval.backends

# url for the git repo to analyze
repo_url = 'http://github.com/grimmoirelab/perceval.git'
# directory for letting Perceval clone the git repo
repo_dir = '/tmp/perceval.git'

# create a Git object, pointing to repo_url, using repo_dir for cloning
repo = perceval.backends.git.Git(uri=repo_url, gitpath=repo_dir)
# fetch all commits as an iteratoir, and iterate it printing each hash
for commit in repo.fetch():
    print(commit['data']['commit'])
```

This code imports the `perceval.backends` module, and then produces an object of the `perceval.backends.git.Git` class. All classes of this kind include a method for fetching the items retrieved by the Perceval backend, as an iterator: `fetch()`. In the last two lines of the script, we iterate through that iterator, printing the hash for all commmits fetched. The output of the script is like:

''`bash
(perceval) $ python3 perceval_git_1.py 
...
26bad088db3df0701f095c7cd45f89e2d9948a7a
bfe38f2e61d2f9743ad5f648880c493085f485b8
18e639396a7fb9a01c4d374baa473fdf7f8b1e10
fdf511b0144cb7707cae1a6b8905e83004cf003b
dd0aec7170367160766a1e155b37db5fa2ae61d9
cedc42d8d897d1bf64e999b91fb9ce34464440c9
d7bef8060648f96000a575b1c2af6bc63f9a0ad3
'''

## Summarizing

In this section we learned to install Perceval in a virtual environment, to run the standalone `perceval` script, and to write our first Python program using Perceval to retrieve items from a data source. In our case, we used the git backend, but other backends are pretty similar. We're now ready for serious stuff...