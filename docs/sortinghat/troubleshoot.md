---
layout: default
title: Troubleshoot
nav_order: 4
parent: SortingHat
---

# Troubleshooting steps

### Profile creation issues

- **Organisation not found**

  ![sortinghat-orgs](./assets/sortinghat-org.png)

The above issue arises when the organisation submitted does not exist in the
`Organisation` table. "Bitergia" here is taken as an example. In order to fix
it, make sure to [add your organisation]({{ site.baseurl }}{% link
docs/sortinghat/affiliations/add.md %}) first, then [create the individuals
profile]().

- **Profile already exist**

  ![sortinghat-sameIdentity](./assets/sortinghat-sameIdentity.png)

  The above issue arises if a existing profile has the exact same information
  (Name, Email, Username, Source etc...) as the profile being created. The ID
  `013d8db4d7fba708448c146c8fb54f8dcb974ed1` refers to the unique identifier of
  a profile.

- **Fields cannot be empty**

  ![sortinghat-no-identity](./assets/sortinghat-no-identity.png)

  The above issue is pretty staightforward. In order to create a profile, a
  minimum amount of information is required which includes, primarily the
  `Source` and any other identity related info (`Name` or `Email` or
  `Username`).