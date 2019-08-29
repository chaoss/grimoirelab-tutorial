## Installing GrimoireLab Python modules

Most of GrimoireLab are Python modules. The easiest way of installing them is using `pip3`,
which will retrieve the corresponding packages from the [Python Package Index](https://pypi.python.org/), and will automatically install them, including their dependencies (other Python packages that they need).

Although it is not needed, we recommend using [Python virtual environments](https://docs.python.org/3/tutorial/venv.html) for installing packages. Below, you can find a section on how to prepare virtual packages in Python3, and then how to install GrimoireLab modules in them. If you are not interested in virtual environments, and know what you are doing, you can skip that part. Only remember, in that case, that it is very likely that you will need to prefix with `sudo` any installation command, to install, as root, in the default location in your system, instead of in a virtual environment.

Most of this section is about installing the packages that are available from
[Pypi](http://pypi.python.org),
which correspond to the period coordinated releases of GrimoireLab.
If you want to install the latest version available in the development
repositories, have a look at
[Installing from development repositories](#repos).

You may need to have some other non-Python packages installed previously. Please check the [section on installing non-Python packages](#non-python-pkgs) if you have any trouble.


### Preparing a virtualenv {#venvs}

I'm assuming you already have Python3 installed,
as detailed in the
[Supporting systems](supporting.html) section. Let's use it to create a Python virtual environment, so that we have a cozy place to work. For that we will use [Python3 venv module](https://docs.python.org/3/library/venv.html).

> _Note:_ Instead of driving the `venv` module directly, you can also use [the pipenv module](http://docs.python-guide.org/en/latest/dev/virtualenvs/#installing-pipenv).

First, let's create our new environment. I like my Python virtual environments under the `venvs` subdirectory in my home directory, and in this case I will call it `gl` \(see how original I am!\):

```bash
$ python3 -m venv ~/venvs/gl
```

Once the virtual environment is created, you can  activate it:

```bash
$ source ~/venvs/gl/bin/activate
(gl) $
```

Now, any Python module you install in that shell will be installed under ~/venvs/grimoirelab, and it will be used by Python only in shells with the virtual environment activated. Since the virtual environment is under your home directory, you won't need to sudo to install: everything will be installed in your name, with your permissions.

When you are done with a virtual environment, you can deactivate it until you need to activate it again. Deactivating is easy:

```bash
(gl) $ deactivate
$
```

Remember that the virtual environment will stay activated only in the shell where you activated it. If you are using several shells \(for example, in several windows\), you can activate the virtual environment as in as many of them as you may want. But all of them will share the Python installation, which means that any module installed in the virtual environment will be available in all the shells where that virtual environment is installed.

You can also have several different virtual environments, each with different sets of Python modules installed. You can use them for different projects, with different dependencies, for example. You just need to activate the one you need when you have to work in the corresponding project.

### Installing tools in the virtual environment

Depending on what you have installed in your system, it may be convenient to install some Python tools in it, and to upgrade some others. We recommend that you type, in your activated virtual environment:

```bash
(gl) $ pip3 install --upgrade pip
(gl) $ pip3 install --upgrade setuptools
(gl) $ pip3 install --upgrade wheel 
```

This will increase the chances that you have no troubles later, when installing wheels (a kind of Python package, used for GrimoireLab modules and many of their dependencies).

### Installing all GrimoireLab modules at once

For installing all GrimoireLab modules, we only need to install, using `pip3`,
the `grimoirelab` package, that pulls all the other GrimoireLab modules as dependencies:

```bash
(gl) $ pip3 install grimoirelab
```

This should install it, and all its dependencies
(which include all of the GrimoireLab modules).
Once installed, check that everything is as it should:

```bash
(gl) $ grimoirelab -v
```

In the following sections, we will explain how to install,
separately, some of the GrimoireLab modules.
Of course, they can be installed in separate virtual environments.
But this is needed only if the `grimoirelab` package was not installed,
and you want to install only some of the modules.

### Installing Perceval

In an activated virtual environment we will use `pip3` to install the module from the [Pypi archive](https://pypi.python.org/pypi).

```bash
(gl) $ pip3 install perceval
```

This will install Perceval and its dependencies \(other Python modules that are needed by Perceval to work\). So, we're ready to see what it can do.

Once Perceval is installed, we can check that the installation went well. For starters, you can use the `perceval` script, which should have been installed, since it comes with the Perceval package. It is a simple front-end to the Perceval module, which gets data from a data source, and writes what it finds as JSON documents in stdout. To learn about its command line arguments, just use the `--help` flag:

```bash
(gl) $ perceval --help
```

This should produce a banner with information about command line arguments, and a listing of Perceval backends. If that banner doesn't show up, it is likely that something wrong happened during the installation.

Assuming everything was fine, next thing is getting information about an specific backend. Let's start with the git backend, which will be a good starter for testing:

```
(gl) $ perceval git --help
```

If this shows a banner with information about how to use the Perceval git backend, we can assume that Perceval and all its dependencies were installed appropriately.

### Installing Graal

Graal can also be installed with `pip3`:

```bash
(gl) $ pip3 install graal
```

Once Graal is installed, you can move ahead to check whether it's installed correctly by simply invoking the module via command line.

```bash
(gl) $ graal --help
```

**Note:** 
1. Graal requires installation of some executables for its execution. More information on installing the executables can be found [here](https://github.com/chaoss/grimoirelab-graal#how-to-installcreate-the-executables). (e.g., cloc)
2. CoLic backend requires executable path of tools which it leverages on ( [NOMOS](https://github.com/fossology/fossology/tree/master/src/nomos) & [SCANCODE](https://github.com/nexB/scancode-toolkit) ). You can install them by following the procedure mentioned [here](https://github.com/chaoss/grimoirelab-graal#how-to-installcreate-the-executables).


### Installing GrimoireELK

GrimoireELK can also be installed with `pip3`.
Again, we will install it in a virtual environment:

```bash
(gl) $ pip3 install grimoire-elk
```

This will pull the `perceval` module, and other dependencies needed, and will install the `grimoire_elk` Python module. It includes the `p2o.py` script, as well, which manages `grimoire_elk` from the command line, and will be fundamental for producing raw and enriched indexes.

### Installing Kidash

Kidash is other package that can be installed with `pip3`:

```bash
(gl) $ pip3 install kidash
```

This will install the `kidash` Python package, which includes the `kidash` Python script and all dependencies needed for it to work. This scripts will allow us to manage dashboards, visualizations, and other elements in Kibana. We will use it to upload dashboard definitions to produce our dashboard in Kibana.

### Installing SortingHat

SortingHat can also be installed with `pip3`:

```bash
(gl) $ pip3 install sortinghat
```

For SortingHat to work, we will also need a MySQL-like database
(we will say just "MySQL" from now on).
In the following, let's assume we have one installed in our own machine (`localhost`).
If your database is anywhere else (eg, in the cloud),
just use its url instead of `localhost` in the examples below.

To check that sortinghat was installed, just run:

```bash
(gl) $ sortinghat --help
```

You should get the banner showing a summary of how to use
the `sortinghat` command.

### Installing Manuscripts

Installation of Manuscripts is easy as well:
just pip3 install the `manuscripts` Python package. In your virtual environment of choice, run:

```bash
(gl) $ pip3 install manuscripts
```

This should install it, and all its dependencies. Once installed, check that everything is as it should:

```bash
(gl) $ manuscripts --help
```

### Installing SirMordred

Installation of SirMordred is no surprise:

```bash
(gl) $ pip3 install sirmordred
```

Once it is installed with its dependencies, try it with:

```bash
(gl) $ sirmordred --help
```

### Installation of non-Python packages {#non-python-pkgs}

Some of GrimoireLab dependencies need non-Python packages as pre-requisites to be installed. Make sure that you have them installed in your system before running the Python installation commands above:

* For `dulwich` to be installed, you need to have some Python libraries present. In Debian-derived systems (such as Ubuntu), that can be done by installing the `python3-dev` package:

```
$ sudo apt-get install python3-dev
```

Usually, you know you need this when you have a problem installing `dulwich`. For example, you check the output of `pip install` and you find:

```
dulwich/_objects.c:21:10: fatal error: Python.h: No such file or Directory
```

`Python.h` is one of the files provided by the `python3-dev` Debian package, which includes development libraries and files needed to compile Python-related code.

### Installing from development repositories {#repos}

Previous instructions are for installing the Python packages corresponding to the GrimoireLab coordinated releases. These packages are supposed to be stable and tested. But if you prefer to live on the edge, you can also install directly from development repositories. To easy this case, there is a little utility: [build_grimoirelab](https://github.com/chaoss/grimoirelab/blob/master/utils/build_grimoirelab).

> **Warning:** latest versions in development repositories may be unstable, not play well with each other, or even not work at all. Use at your own risk.

It is designed to work standalone, with just a few dependencies. It is easy to produce a Python virtual environment with all GrimoireLab tools (and dependencies) installed, corresponding to the latest version in the master branch of each of the development repositories. Just the utility, and run:

```bash
$ python3 build_grimoirelab --install --install_venv /tmp/ivenv
```

This will create a virtual environment in `/tmp/ivenv`, which can be activated as follows
(read above the [basics about virtual environmets](#venvs)).

```bash
$ source /tmp/ivenv/bin/activate
(ivenv) $
  [You can now run arbitrary GrimoireLab commands]
  [For example:]
(ivenv) $ mordred --help
```

`build_grimoirelab` can also be used to create a virtual environment with a specific release of GrimoireLab installed. For that, download the release file (which specifies the versions of each tool) from the
[releases directory](https://github.com/chaoss/grimoirelab/tree/master/releases) and run (assuming you downloaded the release file `elasticgirl.21` to the current directory):

```bash
$ python3 build_grimoirelab --install --install_venv /tmp/ivenv --relfile elasticgirl.21
```

If you want, you can also produce the Python packages (wheels and dists) for any release, or the latest versions in development repositories. For example, for building packages for the latest versions in directory `/tmp/dists`:

```bash
$ python3 build_grimoirelab --build --distdir /tmp/ivenv
```

You can get a listing of all the options of `build_grimoirelab` by using its `--help` flag:

```bash
$ python3 build_grimoirelab --help
```

There is some explanation about some of them in the
[README for the utils directory](https://github.com/chaoss/grimoirelab/blob/master/utils/README.md).
