// Get events.json, and load it in the HTML page
//

function decorate_git (event) {
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
  text += ' (' + project + ', <em>' + repo + '</em>)</p>\n';
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

function decorate_default (event) {
  var text = `<p class="default">`;
  for (var component in event) {
    text += component + ': ';
    text += String(data[event][component])
      .replace(/</g,'&lt;').replace(/>/g,'&gt;');
    text += '</p>\n';
  }
  return(text)
}

$(document).ready(function() {
	$.getJSON("events.json", function(data) {
    var events = '<div class="marquee">';
    for (var event = 0; event < data.length; event++) {
      var event_str = '<div class="event">';
      if ('is_git_commit' in data[event]) {
        event_str += decorate_git(data[event]);
      } else {
        event_str += decorate_default(data[event]);
      }
      event_str += '</div>\n'
      events += event_str + '\n';
    }
    events += '</div>\n';
    $('#events').html(events);
    $('.marquee').css('animation-duration', 4*event + 's')
	});
});
