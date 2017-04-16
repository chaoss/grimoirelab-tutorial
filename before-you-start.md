# Before you start

Before you start working with this training manual, there is some stuff that is convenient to have into account.

* Python version. GrimoireLab is built to run with Python3. Most reasonably recent Python3 versions will work. The examples have been tested with Python 3.5.

* Architecture. GrimoireLab is being developed mainly on GNU/Linux platforms. It is very likely it will work out of the box on any Linux-like (or Unix-like) platform, provided the right version of Python is available. In other platforms, your mileage will vary. We will appreciate experiences of use in any specific architecture (see chapter on Contributing).

* GrimoireLab version. GrimoireLab as such does not have "versions", but its components have. Most recent versions of GrimoireLab components will work, and in general the examples are tested with the latest stable verions available from Pypi. Installing GrimoireELK from Pypi (`pip intall grimoire-elk`) should be enough, since it will pull the right version of Perceval as a dependency. The examples have been tested with GrimoireELK 0.26.5 and Perceval 0.7.0.