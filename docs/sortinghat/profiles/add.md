---
layout: default
title: Creating profiles
nav_order: 1
parent: Profiles and Identities
grand_parent: SortingHat
has_children: false
has_toc: false
---

# How to create a profile

Creating a profile is akin to adding an individual in SortingHat.

To add an individual, click on the **Add** button in the `Individuals` table.
This will open a dialogue titled `Add individual`. Fill in the individual's
respective information and finally click on **Save** to save the information.

![create-profile](../assets/create-profile.png)

In the **Add individual** dialogue,

- `Name`: Name of the individual
- `Email`: Email of the individual
- `Username`: Username of individual with respect to the source
- `Source`: Refers to the data source (github, Telegram, Dockerhub etc...
- `Gender`: Gender of individual
- `Country`: Country where individual resides
- `Bot`: check it if individual is a bot, else leave it be
- `Organization`: organization with which individual is affiliated
- `Date from`: Date when individual started working for mentioned organization
- `Date to`: Date when individual terminated his affiliation with mentioned
  organization

![save-profile](../assets/save-profile.png)

Note: _Organization entered need to be registered in the Organization table
before completing process to add individual. If organization is not present in
organization's table, then individual's data will be saved, **excluding the
organization's data**._