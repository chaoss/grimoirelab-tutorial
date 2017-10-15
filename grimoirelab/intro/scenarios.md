## GrimoireLab scenarios

GrimoireLab is modular not only in the sense that it is composed by modules, but also in the sense that modules can be use separately. To illustrate this, let's visit some different scenarios of how GrimoireLab can be used to analyze software development, from simpler ones, to some of the most complex.

### Perceval analyzing a single data source

In this case, we will use just Perceval, as a Python module, to retrieve information from one data source. For example, that can be a git repository, a GitHub project, or a mailing list.

![](/grimoirelab/grimoirelab-fit-perceval-1.png)

As can be seen in the figure above, data retrieved by Perceval is consumed by a Python script, which will produce the output needed. In this simple scenario, most of the components in GrimoireLab are not needed, and the setup is rather simple: just the Perceval Python module needs to be installed. This is the case explained in sections [Retriving git metadata](/training/perceval/git.md), [Retrieving data from GitHub repositories](/training/perceval/github.md) and [Mail archives](/training/perceval/mail.md)