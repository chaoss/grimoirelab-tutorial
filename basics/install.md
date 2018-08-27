## Installing GrimoireLab Python modules

Most of GrimoireLab are Python modules. The easiest way of installing them is using `pip3`,
which will retrieve the corresponding packages from the [Python Package Index](https://pypi.python.org/), and will automatically install them, including their dependecies (other Python packages that they need).

Although it is not needed, we recomend using [Python virtual environments](https://docs.python.org/3/tutorial/venv.html) for installing packages. Below, you can find a section on how to prepare vitual packages in Python3, and then how to install GrimoireLab modules in them. If you are not interested in virtual environments, and know what you are doing, you can skip that part. Only remember, in that case, that it is very likely that you will need to prefix with `sudo` any installation command, to install, as root, in the default location in your system, instead of in a virtual environment.

Most of this section is about installing the packages that are available from [Pypi](http://pypi.python.org), which correspond to the period coordinated releases of GrimoireLab. If you want to install the latest version available in the development repositories, have a look at [Installing from development repositories](#install-devel-repos).


### Preparing a virtualenv
<a name="venvs"></a>

I'm assuming you already have Python3 installed, as detailed in the [Supporting systems](/before-you-start/supporting-systems.md) section. Let's use it to create a Python virtual environment, so that we have a cozy place to work. For that we will use [Python3 venv module](https://docs.python.org/3/library/venv.html).

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

Depending on what you have installed in your system, it may be convenient to install some Python tools in it, and to upgrade some others. We recommend that you type, in your activated virtual ennvironment:

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
and you want to install only some of the modueles.

### Installing Perceval

In an activated virtual environment we will use `pip3` to install the module from the [Pypi archive](https://pypi.python.org/pypi).

```bash
(gl) $ pip3 install perceval
```

This will install Perceval and its dependencies \(other Python modules that are needed by Perceval to work\). So, we're ready to see what it can do.

Once Perceval is installed, we can check that the installation went well. For a starter, you can use the `perceval` script, which should have been installed, since it comes with the Perceval package. It is a simple front-end to the Perceval module, which gets data from a data source, and writes what it finds as JSON documents in stdout. To learn about its command line arguments, just use the `--help` flag:

```bash
(gl) $ perceval --help
```

This should produce a banner with information about command line arguments, and a listing of Perceval backends. If that banner doesn't show up, it is likely that something wrong happened during the installation.

Assuming everything was fine, next thing is getting information about an specific backend. Let's start with the git backend, which will be a good starter for testing:

```
(gl) $ perceval git --help
```

If this shows a banner with information about how to use the Perceval git backend, we can assume that Perceval and all its dependencies were installed appropriately.

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


### Installing from development repositories
<a name="install-devel-repos"></a>

Previous instructions are for installing the Python packages corresponding to the GrimoireLab coordinated releases. These packages are supposed to be stable and tested. But if you prefer to live in the edge, you can also install directly from development repositories. To easy this case, there is a little utility: [build_grimoirelab](https://github.com/chaoss/grimoirelab/blob/master/utils/build_grimoirelab).

> **Warning:** latest versions in development repositories may be instable, not play well with each other, or even not work at all. Use at your own risk.

It is designed to work standalone, with just a few dependencies. It is easy to produce a Python virtual environment with all GrimoireLab tools (and dependencies) installed, corresponding to the latest version in the master branch of each of the development repositories. Just the utility, and run:

```bash
$ python3 build_grimoirelab --install --install_venv /tmp/ivenv
```

This will create a virtual environment in `/tmp/ivenv`, which can be activated as follows (read above the [basics about virtual environmets](#venvs)).

```bash
$ source /tmp/ivenv/bin/activate
(ivenv) $
  [You can now run arbitrary GrimoireLab commands]
  [For example:]
(ivenv) $ mordred --help
```

`build_grimoirelab` can also be used to create a virtual enviroment with a specific release of GrimoireLab installed. For that, download the release file (which specifies the versions of each tool) from the[releases directory](https://github.com/chaoss/grimoirelab/tree/master/releases) and run (assuming you downloaded the release file `elasticgirl.21` to the current directory):

```bash
$ python3 build_grimoirelab --install --install_venv /tmp/ivenv --relfile elasticgirl.21
```

If you want, you can also produce the Python packages (wheels and dists) for any release, or the latest versions in development repositories. For example, for building packages for the latest versions in directory `/tmp/dists`:

```bash
$ python3 build_grimoirelab --build --distdir /tmp/ivenv
```

You can get a listing of all the options of `build_grimoirelab' by using its `--help` flag:

```bash
$ python3 build_grimoirelab --help
```

There is some explanation about some of them in the
[README for the utils directory](https://github.com/chaoss/grimoirelab/blob/master/utils/README.md).
