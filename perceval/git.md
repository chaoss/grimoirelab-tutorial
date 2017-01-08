# Retriving git metadata

Git is the most popular source code management system. Is is usually used to track versions of source code files. Transactions on a git repositories are called "commits". Each commit is an atomic change to the files in the repository. For each commit, git maitains data for tracking what changed, and some metadata about who committed the change, when, which files were affected, etc. Perceval retrieves this information, and produces a JSON document \(a Python dictionary\) for each commit.

