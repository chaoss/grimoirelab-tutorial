## A dashboard with SortingHat

The simple dashboard we just produced uses indexes which do not benefit from SortingHat, because it was not used to produce them. SortingHat is the GrimoireLab component that manages identities, allowing for merging of identities, definition of profiles for each person, and of periods of affiliation (when people worked for which organization).

SortingHat uses a MySQL-like database ([MySQL](https://www.mysql.com/) or MariaDB, for example).