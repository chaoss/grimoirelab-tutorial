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


## Summarizing

In this section we learned to install Perceval in a virtual environment, to run the standalone `perceval` script, and to write our first Python program using Perceval to retrieve items from a data source. In our case, we used the git backend, but other backends are pretty similar. We're now ready for serious stuff...