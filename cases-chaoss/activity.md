## Community Activity

Once we have the indexes, let's create the first panel, for community activity.

As usual with Kibana/Kibiter (from now own Kibiter) we will enter it in edit mode, import the produced indexes as index patterns, and proceed to create the visualizations and dashboards.

Alternatively, you can instead use the [chaoss_community_activity.json](https://github.com/chaoss/grimoirelab-tutorial/blob/master/cases-chaoss/dashboards/chaoss_community_activity.json) file, which stores the configuration for all the index patterns, visualizations and dashboard. If you decide to shortcut this way, just install it with `kidash.py`:

```bash
(gl) $ kidash.py --elastic_url http://localhost:9200 \
  --import chaoss_community_activity.json --debug
```

This will import evertything into Kibana, and the dashboard will be now visible with the name `chaoss_community_activity'.

Or you can produce everything yourself, as explained below.

### Index patterns

In this case, it will be easy. As usual, click on `Management` on the left menu, and then on `Index patterns`.

![](/cases-chaoss/index_patterns.png)

Once there, `Create new index`. You will do this twice: once for the index pattern `git`, and the other one for `github`, which are the enriched indexes we created with `p2o.py`. In both cases, specify `grimoire_creation_date` as the time field.

Once this is done, you should be able of seeing both index patterns if you click on the `Discover` option of the left menu.

![](/cases-chaoss/discover_indexes.png)

### Visualizations

This will be even easier. We will create a Markdown visualization for the text explaining the metric represented in this panel, and three visualizations for each of the three activity items to represent (git commits, GitHub issues and GitHub pull requests):

* Metrics visualization, with the total number of items. For commits, use `Unique count` on the `hash` field, since we want to avoid double counting commits which happen to be in several repositories. For others, just use `Count`.
* Horizontal bars visualization, with the time series of items over time. Again, use `Unique count` for commits, as above, and `Count` for the others.
* Table visualization, with the items per repository, for filtering purposes. Just bucket by the  `github_repo` field, and use `Count` as aggregator.

For commits, you can just use the `git` index pattern as the base for the visualizations. But for issues and pull requests we need a little trick, since both are together in the `github` index pattern (the GitHub API Perceval uses provides all mixed). It is just to add a filter to the visualizations (use the `Add filter` button on the top left), setting it to `pull_request` (field) `is one of` `false`, for issues, and `true` for pull requests.

And you are done.

# Dashboard

Producing the dashboard is just a matter of (still in Kibiter edit mode), click on the `Dashboards` option in the left menu, and create a new one. Add to it all the visualizations we just created, and ready. The result is as shown below.

![](/cases-chaoss/dashboard_chaoss_community_activity.png)

The default period is 6 months, but since the dashboard is querying the database live, it is easy to select some other time frame. For example, go to the top right and select "last two years".

![](/cases-chaoss/dashboard_chaoss_community_activity-2y.png)

Or youn can filter for a single repository (or everything except for a repository, or other combinations). For example, to examine the activity only in the Perceval repository, click on the `+` that appears when you hover the pointer over `grimoirelab/perceval` in any of the tables on the right. You'll get a filter (see in the top left) for that repository, and now all the metrics are only for it.

![](/cases-chaoss/dashboard_chaoss_community_activity-2y-perceval.png)

Enjoy!
