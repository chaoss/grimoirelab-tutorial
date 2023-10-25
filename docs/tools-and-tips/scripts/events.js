// Get events.json, and load it in the HTML page as a vertical marqee
// Do that continuously, checking for new events in new events.json
//

// Copyright (C) 2017 Bitergia
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
//
// Authors:
//   Jesus M. Gonzalez-Barahona <jgb@bitergia.com>
//

(function() {

  // Variable for events to show in marquee
  var events = [];
  // Element for the marquee
  var marquee_el;
  // Last height of marquee_el
  var marquee_height = 0;

  // Decorate a git event (produce HTML from it)
  function decorate_git (event) {
    var date = new Date(event['date']);
    var author = event['author_name'];
    var org = event['author_org_name'];
    var project = event['project'];
    var repo = event['repo_name'];
    var hash = event['hash'].slice(0,7);
    var commit_date = new Date(event['utc_commit'])
    var author_date = new Date(event['utc_author'])
    var message = event['message']
      .replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/(?:\r\n|\r|\n)/g,'<br>');

    var text = '<p class="head">Commit: <b>' + hash + '</b> ';
    text += ' (' + project + ', <em>' + repo + '</em>)</br>\n';
    text += String(date) + '</p>\n';
    text += '<p class="author">Author: ' + author + ' (' + org + ')</p>\n';
    text += '<p class="date">Commit date: <em>' + String(commit_date)
      + '</em></p>\n';
    text += '<p class="date">Author date: <em>' + String(author_date)
      + '</em></p>\n';
    time_diff = (commit_date.getTime() - author_date.getTime()) / (1000 * 3600 * 24)
    text += '<p class="date">Days from authorship to commit: <em>'
      + time_diff.toFixed(2) + '</em></p>\n';
    text += '<p class="message">' + message + '<p>\n';

    return(text)
  }

  // Decorate a "generic" event (produce HTML from it)
  function decorate_default (event) {
    var text = `<p class="default">`;
    for (var component in event) {
      text += component + ': ';
      text += String(data[event][component])
        .replace(/</g,'&lt;').replace(/>/g,'&gt;');
      text += '</p>\n';
    }
    return(text);
  }

  // Update the text to appear in the marquee with some events
  function update_marquee (el, events) {
    var event_str;
    var event_el;

    for (var event = 0; event < events.length; event++) {
      if ('is_git_commit' in events[event]) {
        event_str = decorate_git(events[event]);
      } else {
        event_str = decorate_default(events[event]);
      }
      event_el = $('<div />').addClass('event').html(event_str);
      el.append(event_el);
    };
  };

  // Update the marquee.
  // get events.json, decide which ones are new events,
  // decorate those, update the marquee, and call itself,
  // for further updating
  function update () {
    $.getJSON("events.json", function(data) {
      var new_events = [];

      console.log("Update");
      if (events.length == 0) {
        console.log("Intializing events")
        events = data;
        new_events = data;
      } else {
        console.log("Considering updating events")
        last_date = events[events.length-1]['date'];
        for (var event = 0; event < data.length; event++) {
          if (data[event]['date'] > last_date) {
            console.log("Updating event")
            events.push(data[event])
            new_events.push(data[event]);
          };
        };
      };
      update_marquee(marquee_el, new_events);
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

  // When the DOM is ready, start the show
  $(document).ready(function(){
    $.ajaxSetup({cache: false});
    var events_el = $('#events').first();
    events_el.html('<div class="marquee"></div>');
    marquee_el = events_el.children().first();
    console.log(events_el.height());
    update();
  });

})();
