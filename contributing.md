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

# Contributors

* The example about producing a dashboard for Meetup was contributed by
  [Manrique López de la Fuente](https://twitter.com/jsmanrique)
  ([Bitergia](http://bitergia.com)) in March 2017.

* The section on Perceval backend is based on a contribution by
  [Valerio Cosentino[(https://github.com/valeriocos)([Bitergia](http://bitergia.com))
  in October 2017.
