# First steps with Perceval

Being a Python module, to use Perceval you will need to have Python installed in your system. Once this is the case, Perceval will be installed as a module, using `pip`, the standard mechanism for installing modules for Python. Below, you will learn to install the module using a virtual environment \(which is convenient, but not mandatory\), and testing that it was properly installed. If you prefer not to work with virtual environments just skip the next section, and go straight to the installation instructions. Only remember that it is very likely that you will need to prefix with `sudo` any installation command, to install, as root, in the default location in your system, instead of in a virtual environment.

## Preparing a virtualenv

I'm assuming you already have Python3 installed \(Perceval is written for Python3\). Let's start by creating a Python virtual environment, so that we have a cozy place to work. In the following, we will use [Python3's pyvenv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) \(available in Debian or Ubuntu as the `python3-venv` package\). But using the more traditional [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) should be possible as well.

First, let's create our new environment. I like my Python virtual environments under the `venvs` subdirectory in my home directory, and in this case I will call it `perceval` \(see how original I am!\):

```bash
$ pyvenv ~/venvs/perceval
```

Once the virtual environment is created, you can  activate it:

```Bash
$ source ~/venvs/perceval/bin/activate
(perceval) $
```

Now, any Python module you install in that shell will be installed under ~/venvs/perceval, and will be used by Python only in shells with the virtual environment activated. Since the virtual environment is under your home directory, you won't need to sudo to install: everything will be installed in your name, with your permissions.

When you are done with a virtual environment, you can deactivate it until you need to activate it again. Deactivating is easy:

```Bash
(perceval) $ deactivate
$
```

Remember that the virtual environment will stay activated only in the shell where you activated it. If you are using several shells \(for example, in several windows\), you can activate the virtual environment as in as many of them as you may want. But remember that all of them will share the Python installation, which means that any module installed in the virtual environment will be available in all the shells where that virtual environment is installed.

You can also have several different virtual environments, each with different sets of Python modules installed. You can use them for different projects, with different dependencies, for example. You just need to activate the one you need when you have to work in the corresponding project.

## Installing Perceval

Once activated, install Perceval, which will therefore be present only in your virtual environment. For installing Perceval, we will use pip, which will install it from the [Pypi archive](https://pypi.python.org/pypi).

```bash
(perceval) $ pip3 install perceval
```

This will install Perceval and its dependencies \(other Python modules that are needed by Perceval to work\). So, we're ready to see what it can do.

## Checking that it is installed

Once Perceval is installed, we can check that the installation went well. For a starter, you can use the `perceval` script, which should have been installed, since it comes with the Perceval package. It is a simple front-end to the Perceval module, which gets data from a data source, and writes what it finds as JSON documents in stdout. To learn about its command line arguments, just use the `--help` flag:

```bash
(perceval) $ perceval --help
```

This should produce a banner with information about command line arguments, and a listing of Perceval backends. If that banner doesn't show up, it is likely that something wrong happened during the installation.

Assuming everything was fine, next thing is getting information about an specific backend. Let's start with the git backend, which will be a good starter for testing:

```
(perceval) $ perceval git --help
```

If this shows a banner with information about how to use the Perceval git backend, we can assume that Perceval and all its dependencies were installed appropriately.

Now that we have Perceval installed, let's give it a try. For that, in the following sections we will use it to retrieve information from some kinds of repositories. You're on your way to software development analysis!

