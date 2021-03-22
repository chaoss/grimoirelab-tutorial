## HTML5 app: latest activity

Let's build a simple HTML5 app showing the latest activity of a project or a set of projects. For that, we will create in fact two applications:

![](/tools-and-tips/html5_app_moving.gif)

* A Python application to produce a JSON document by querying one or more indexes with information about the latest activity ([`elastic_last.py`](https://github.com/jgbarah/GrimoireLab-training/blob/master/tools-and-tips/scripts/elastic_last.py)).
* A HTML5 application showing the contents of that JSON document in a vertical marquee ([`index.html`](https://github.com/jgbarah/GrimoireLab-training/blob/master/tools-and-tips/scripts/index.html) and related files, see below).

### Deploying everything

For demoing the application, you can first install the files for the HTML application, export them via a web server (so that the application can be loaded in a browser), and produce a JSON file with the latest events of your dashboard of choice. Let's assume we already have a deployed dashboard. We will get our latest events from it. If you don't have access to one of them, just use the data in [Producing Kibana dashboards](https://chaoss.github.io/grimoirelab-tutorial/gelk/intro.html).

For deploying the HTML5 app, just copy `index.html`, `events.js`, and `events.css`, all in the [`scripts`](https://github.com/jgbarah/GrimoireLab-training/blob/master/tools-and-tips/scripts/) directory, to your directory of choice. Then, ensure that some web server is serving that directory. For example, you can launch a simple Python server from it:

```bash
$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 ...
```

Now, let's produce a JSON file with the events that the app will show. For that, we will install [`elastic_last.py`](https://github.com/jgbarah/GrimoireLab-training/blob/master/tools-and-tips/scripts/elastic_last.py) in a Python3 virtual environment with all the needed dependencies (in this case, it is enough to install, via `pip`, the `elasticsearch-dsl` module, and run it:

```
$ python3 elastic_last.py --loop 10 --total 10 http://localhost:9200/git
```

(assuming ElasticSearch is running in the same host, in port 9200, as it runs by default, and that it has an index, named `git` with the standard git index, as produced by GrimoireELK)

If we're using a `git` index in an ElasticSearch instance accessible at `https://grimoirelab.biterg.io/data`, using user `user` and password `XXX`:

```
$ python3 elastic_last.py --no_verify_certs --loop 10 --total 10 \
https://user:XXX@grimoirelab.biterg.io/data/git
```

In both cases `--loop 10` will cause the script to retrieve the index every 10 seconds, and produce a file `events.json` with the latest 10 events in the index (commits in this case), because of the option `--total 10`. If you want, instead of just one url, you can include as many as you may want, one after the other, to retrieve data from several indexes every 10 seconds. The option `--no_verify_certs` is needed only if your Python installation has trouble checking the validity of the SSL certificates (needed because the url is using HTTPS).

The result will be similar to:

![](/tools-and-tips/html5_app_moving.gif)

### Get latest activity

The script retrieving the latest activity is simple. Most of the action happens in this loop (simplified):

```python
    while loop:
        results = []
        for url in args.urls:
            results.extend(last_items(url, args.verify_certs,
                        args.date_field, args.count))
        sorted_results = sorted(results, key=operator.itemgetter(args.date_field))
        output_results = sorted_results[-args.total:]
        json_results = json.dumps(output_results, sort_keys=True, indent=2)
        with open(args.output, 'w') as f:
            f.write(json_results)
        ...
```

That is: for all the urls in the command line, get the last items from the corresponding indexes, and add them to `results`. Once the for loop is done, `results` will have a list with all the events obtained from the indexes. Then, it is only a matter of sorting them by date (the script allows to decide which field to use for sorting), and then just get as many as specifified by `--total` and write them to `events.json` as a JSON string.

`last_items` is the function actually retrieving events from the indexes (simplified):

```python
def last_items(url, verify_certs, date_field, count):

    es = elasticsearch.Elasticsearch([es_url], verify_certs=verify_certs)
    request = elasticsearch_dsl.Search(using=es, index=index)
    request = request.sort('-' + date_field)
    request = request[0:count]
    response = request.execute()
    results = []
    for item in response:
        item['date'] = item[date_field]
        results.append(item.to_dict())
    return results
```

Create a request to ElasticSearch using `elasticsearch-dsl`, specifying that you want results ordered by `date_field` (inverse), and of those get only the first `count` items. Then, for all the items in the ElasticSearch response, annotate each with a new field `date` (which will be used to store the date consdiered for the ordering). And that's it.

The rest is just parsing arguments and ancilliary code to have reasonable code. Easy, isn't it?

The result is a JSON file wihcih specifies a a list of events, each encoded as an object (coming from the corresponding Python dictionary).

### HTML5 app

The HTML5 app is basically a loop retrieving `events.json`, parsing it, and writting the events (after some HTML formating) into the HTML structure which will show them as a marquee.

For the code, we rely on [jQuery](http://jquery.com), which offers a convenient [`animate()`](http://api.jquery.com/animate/) function which will be the basis of the marquee.

HTML is pretty simple (still more simplified):

```html
<!DOCTYPE html>

<html lang="en-US">
  <head>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script type="text/javascript" src="events.js"></script>
  </head>

  <body>
    <div class="page-wrapper">

      <header>
        <h1>GrimoireLab Last Events Demo</h1>
	<h2>Because knowledge empowers</h2>
      </header>

      <div class="summary">
	<p>A demonstration ....</p>
      </div>

      <div class="preamble">
        <div id="events"></div>
      </div>
    </div>
  </body>
</html>
```

The `events` div element will be filled by the JavaScript code with the marquee which will show the events in `events.json`. When that is done, the static aspect of the page will be like this (decoration thanks to `events.json`:

![](/tools-and-tips/html5_app.png)

The animation will be the business of the `animate()` Javascript code. Let's have a look at that code in `events.js` (remember that this code runs using jQuery). The code is activated once the DOM is ready (simplified):

```javascript
  $(document).ready(function(){
    var events_el = $('#events').first();
    events_el.html('<div class="marquee"></div>');
    marquee_el = events_el.children().first();
    update();
  });
```

It is simple to understand: locate the first element in the class `events`, insert a `div` of class `marquee` in it (to insert the element for the marquee), store it in a variable (`marquee_el`) and run `update()`.

The structure of `update()` is as follows

```javascript
function update () {
    $.getJSON("events.json", function(data) {
      var new_events = [];

      if (events.length == 0) {
        events = data;
        new_events = data;
      } else {
        last_date = events[events.length-1]['date'];
        for (var event = 0; event < data.length; event++) {
          if (data[event]['date'] > last_date) {
            events.push(data[event])
            new_events.push(data[event]);
          };
        };
      };
      update_marquee(marquee_el, new_events);
```

That is: get the `events.json` file, and when done, if we have nothing in the `events` global variable (first time we get this file), just copy all events to `new_events`. If we already have some events, push to `new_events` only thos which are new. Then, use those new events to update the marquee (just by writting them as `div` elements in it, see details in `update_marquee()`). Note that jQuery did the trick of converting the incoming `events.json` file into the `data` object, which allows for the access to all events as objects in a list (as they were packed in the JSON file).

The rest of the code in `update()` deals with defining the parameters for `animate()`:

```javascript
      var new_marquee_height = marquee_el.height();
      var inc_marquee_height = new_marquee_height - marquee_height;
      marquee_height = new_marquee_height;
      console.log(marquee_height, inc_marquee_height);
      if (inc_marquee_height > 0) {
        var timeout = inc_marquee_height * 50;
        marquee_el.animate({
          bottom: marquee_el.height()-150
        }, {
          duration: timeout,
          easing: "linear",
          complete: update
        });
      } else {
        setTimeout(update, 1000*10);
      };
  	});
  }
```

This code also decides when to call to `update()` next time: once the marquee was completely shown, or if it already was, in 10 seconds. So, we can now understand what the app does in terms of updating the information: it first retrieves `events.json`, and shows all the events in it. When it is done, retrieves a new version of the JSON file, and shows the new events in it, if any. If there was no new event, waits for 10 seconds, and retrieve the JSON file once again, until there are some new events in it, when they are shown by continuing the marquee.

So, we will see the marquee rolling until no new eevents come in `events.json`, when it will stop for at a certain number of 10 seconds periods, until new events come again, which will make the marquee to roll again. And so on.

Funnny, isn't it?
