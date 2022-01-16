---
layout: default
title: Filter through profiles
nav_order: 8
parent: Profiles and Identities
grand_parent: SortingHat
has_children: false
has_toc: false
---

# Filter through profiles

SortingHat provides several filters which can be used to filter through the
lists of individuals to find the required one. You can filter through the
profiles according to the following filters.

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">isBot</code>

  Filter profiles marked as bots. For example `isBot: true` will return all profiles marked as bot and vice versa.

  ![is-bot](../assets/is-bot.png)

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">isLocked</code>
  
  Filter profiles marked as locked. For example `isLocked: true` will return all profiles marked as locked and vice versa.

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">country</code>

  Filter profiles according to country of residence. For example `country: "United States of America` or `country: USA` return individuals from the United States.

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">gender</code>

  Filter profiles based on their gender. For example `gender: non binary`

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">source</code>

  Filter profiles based on data source. For example `source: Github`

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">enrollment</code>

  Filter profiles based on organizations. For example `enrollment: "Bitergia"`

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">isEnrolled</code>

  Filter profiles based on enrollment status. For example `isEnrolled: true` will return all profiles currently enrolled at some organization and vice versa

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">enrollmentDate</code>

  Filter profiles based on when they were affiliated to an organization.

  | Filter                                             | Explanation                                                                              |
  | -------------------------------------------------- | ---------------------------------------------------------------------------------------- |
  | `enrollmentDate:>YYYY-MM-DD`            | Matches individuals that were affiliated to an organization after the given date.        |
  | `enrollmentDate:>=YYYY-MM-DD`           | Matches individuals that were affiliated to an organization on or after the given date.  |
  | `enrollmentDate:<YYYY-MM-DD`         | Matches individuals that were affiliated to an organization before the given ;date.      |
  | `enrollmentDate:<=YYYY-MM-DD`           | Matches individuals that were affiliated to an organization on or before the given date. |
  | `enrollmentDate:YYYY-MM-DD..YYYY-MM-DD` | Matches individuals that were affiliated to an organization between the given dates      |

- <code style="background-color: #FBE5E1; color: #C0341D; padding: 0 0.4rem; font-size:15px;">lastUpdated</code>

  Filter profiles based on when they were last updated.

  | Filter                                          | Explanation                                                       |
  | ----------------------------------------------- | ----------------------------------------------------------------- |
  | `lastUpdated:>YYYY-MM-DD`            | Matches individuals that were updated after the given date        |
  | `lastUpdated:>=YYYY-MM-DD`           | Matches individuals that were updated on or after the given date. |
  | `lastUpdated:<YYYY-MM-DD`         | Matches individuals that were updated before the given date.      |
  | `lastUpdated:<=YYYY-MM-DD`           | Matches individuals that were updated on or before the given date |
  | `lastUpdated:YYYY-MM-DD..YYYY-MM-DD` | Matches individuals that were updated between the given dates.    |
