# Contributing to GrimoireLab Tutorial

This tutorial is built using 
[Markdown syntax](https://guides.github.com/features/mastering-markdown/), 
[Jekyll](https://jekyllrb.com/), and 
[pmarsceill/just-the-docs](https://github.com/pmarsceill/just-the-docs) theme.

All the Markdown files and Jekyll configuration files are maintained in the 
[chaoss/grimoirelab-tutorial](http://github.com/chaoss/grimoirelab-tutorial) 
GitHub repository.

All Contributions are welcome! You can open 
[pull requests](https://github.com/chaoss/grimoirelab-tutorial/pulls) to add 
the related content. Feel free to open 
[issues](https://github.com/chaoss/grimoirelab-tutorial/issues), to report some 
bug, to propose some enhancement, to ask for some new content, or just to comment 
or suggest something. Any feedback is appreciated!

If you are willing to setup the tutorial locally
```bash
$ git clone https://github.com/chaoss/grimoirelab-tutorial
$ cd grimoirelab-tutorial
$ bundle
$ bundle exec jekyll serve
```

**Note:** Make sure you have git and ruby (version 2.7.x) installed.

This will produce the HTML files, and run an HTTP server that will serve them 
in http://localhost:4000.

## Quick start for contributing

These are the basic steps to set up a developing and testing environment to 
contribute, using GitHub facilities. You can read more details about how to 
contribute to a project in GitHub in 
[How to GitHub: Fork, Branch, Track, Squash and Pull Request](https://gun.io/blog/how-to-github-fork-branch-and-pull-request).

1. Fork the tutorial repository on GitHub. You can use the GitHub web interface 
for this. The result will be a new repository with the rest of your repositories, 
which is a fork (copy) of the GrimoireLab Tutorial.

2. Clone the forked git repository, and create in a local branch for your 
contribution.

```
$ git clone https://github.com/username/grimoirelab-tutorial/
$ cd grimoirelab-tutorial/
$ git checkout -b new-branch-name
```

3. In this repository, set up a remote for the upstream (original grimoirelab-tutorial) 
git repository.

```
$ git remote add upstream https://github.com/chaoss/grimoirelab-tutorial/
```

4. Now you can change the documentation and then commit it. Except that the 
contribution really needs it, use a single commit, and comment in detail in the 
corresponding commit message what it is intended to do. If it fixes some bug, 
reference it (with the text "_Fixes #23_", for example, for issue number 23).

```
$ git add -A
$ git commit -s
```

5. Once your contribution is ready, rebase your local branch with `upstream/master`, 
so that it merges clean with that branch, and push your local branch to a remote 
branch to your GitHub repository.

```
$ git fetch upstream
$ git rebase upstream/master
$ git push origin new-branch-name
```

6. In the GitHub interface, produce a pull request from your branch (you will 
see an option to do that if you visit the webpage for your own repository in 
GitHub). Be sure of including a reasonable comment with the pull request.

7. Visit frequently the pull request in GitHub, to attend to comments and requests 
by GrimoireLab Tutorial developers (or watch it via email).

8. Please keep in mind 
the the pull request will be merged into the codebase only if those comments and 
requests are addressed.

## DCO and Sign-Off for contributions

The [CHAOSS Charter](https://github.com/chaoss/governance/blob/master/project-charter.md) 
requires that contributions are accompanied by a 
[Developer Certificate of Origin](http://developercertificate.org) sign-off. 
For ensuring it, a bot checks all incoming commits.

For users of the git command line interface, a sign-off is accomplished with the 
`-s` as part of the commit command:

```
git commit -s -m 'This is a commit message'
```

For users of the GitHub interface (using the "edit" button on any file, and producing 
a commit from it), a sign-off is accomplished by writing

```
Signed-off-by: Your Name <YourName@example.org>
```

in a single line, into the commit comment field. This can be automated by using a 
browser plugin like [DCO GitHub UI](https://github.com/scottrigby/dco-gh-ui).

## Contributing Guidelines

These are some general guidelines and information related to how we contribute 
to GrimoireLab. You can read about it from the 
[CONTRIBUTING.md](https://github.com/chaoss/grimoirelab/blob/master/CONTRIBUTING.md).
