# How to contribute

This training manual is built using
[Markdown syntax](https://www.gitbook.com/book/gitbookio/markdown/),
and the [Documentation Theme for Jekyll](https://idratherbewriting.com/documentation-theme-jekyll/),
for rendering the HTML pages.
All the Markdown files and Jekyll configuration files are maintained in the
[chaoss/grimoirelab-tutorial GitHub repository](http://github.com/chaoss/grimoirelab-tutorial).

[Pull requests to that repository](https://github.com/chaoss/grimoirelab-tutorial/pulls)
are welcome. If you prefer, you can also open
[some issue on it](https://github.com/chaoss/grimoirelab-tutorial/issues),
to report some bug, to propose some enhancement, to ask for some new content,
or just to comment or suggest something. Any feedback is appreciated!

If you want to produce your own version of the HTML pages from the sources,
ensure you have Ruby installed, and:

```bash
% git clone https://github.com/chaoss/grimoirelab-tutorial
% cd grimoirelab-tutorial
% bundle exec jekyll serve
```

This will produce the HTML files, and run an HTTP server
that will serve them in http://localhost:4000

## DCO and Sign-Off for contributions

The [CHAOSS Charter](https://github.com/chaoss/governance/blob/master/project-charter.md) requires that contributions
are accompanied by a [Developer Certificate of Origin](http://developercertificate.org) sign-off.
For ensuring it, a bot checks all incoming commits.

For users of the git command line interface, a sign-off is accomplished with the `-s` as part of the commit command: 

```
git commit -s -m 'This is a commit message'
```

For users of the GitHub interface (using the "edit" button on any file, and producing a commit from it),
a sign-off is accomplished by writing

```
Signed-off-by: Your Name <YourName@example.org>
```

in a single line, into the commit comment field. This can be automated by using a browser plugin like
[DCO GitHub UI](https://github.com/scottrigby/dco-gh-ui).


# Contributors

* The example about producing a dashboard for Meetup was contributed by
  [Manrique López de la Fuente](https://twitter.com/jsmanrique)
  ([Bitergia](http://bitergia.com)) in March 2017.

* The section on Perceval backend is based on a contribution by
  [Valerio Cosentino[(https://github.com/valeriocos)([Bitergia](http://bitergia.com))
  in October 2017.
