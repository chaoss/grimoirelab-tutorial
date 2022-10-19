## Perceval

This section shows some scripts using Perceval.

### Git commit counter.

[perceval_git_counter](https://github.com/jgbarah/GrimoireLab-training/blob/master/tools-and-tips/scripts/perceval_git_counter.py) is a simple utility to count commits in a git repository. Just run it with the url of the repository to count, and a directory to clone, and you're done:

```bash
python perceval_git_counter.py https://github.com/grimoirelab/perceval.git /tmp/ppp 
# Number of commmits: 579.
```

You can get a help banner, including options, by running

```bash
python perceval_git_counter.py --help
```

There is an option to print commit hashes for all commits in the repository: `--print`.

This utility illusrates how the generator provided by Perceval classes for the different kinds of repositories can be used to run through all the items in them.