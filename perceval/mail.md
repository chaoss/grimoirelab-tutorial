# Mail archives

Many software development projects use mailing lists as a mean for coordination. Mailing lists can be archived in many different ways, but maybe the most classical is using the mbox format. This format is simple: messages are stored in a file with the beginning of each one indicated by a line starting with the string “From ”. Perceval has a backend for supporting mbox archives, with the imaginative name `mbox`. Unfortunately, there are several variations of the basic format: Perceval does its best for parsing all those variations.

## Parsing mbox archives


As in other cases, we can start by asking Perceval for some help:

```
(perceval) $ perceval mbox --help
```

From the banner it produces, we learn that the most simple usage is specifying the uri for the mailing list to analyze, and a directory with its archives. The uri is used mainly for annotation purposes, and can really be any string. The directory needs to be filled with files, each of them in mbox format. So, let's start by getting one archive:

```bash
(perceval) $ mkdir archives
(perceval) $ wget -P archives http://mail-archives.apache.org/mod_mbox/httpd-announce/201607.mbox
```

These two lines (assuming we already have wget installed), will retrieve the archive corresponding to July 2016 of the mailing list `httpd-announce`, of the Apache project. The option `-P archives` to wget will ensure that the file is stored in the `archives` directory, which we created in the previous line.

Once we have the archive, we can analyze it:

```bash
(perceval) $ perceval mbox httpd-announce archives > perceval.log
[2016-11-23 02:12:02,476] - Sir Perceval is on his quest.
[2016-11-23 02:12:02,477] - Looking for messages from 'httpd-announce' on 'archives' since 1970-01-01 00:00:00+00:00
[2016-11-23 02:12:02,488] - Done. 4/4 messages fetched; 0 ignored
[2016-11-23 02:12:02,488] - Fetch process completed
[2016-11-23 02:12:02,488] - Sir Perceval completed his quest.
```

The above message show how the `archives` directory was parsed looking for mbox files, how 4 messages were found, of which none was ignored. Since the output was redirected to `perceval.log`, now we have the JSON documents produced by Perceval in that file:

```
{
    "backend_name": "MBox",
    "backend_version": "0.6.0",
    "category": "message",
    "data": {
        "Authentication-Results": "spamd4-us-west.apache.org (amavisd-new);\n\tdkim=pass (2048-bit key) header.d=comcast.net",
        "Content-Transfer-Encoding": "7bit",
        "Content-Type": "text/plain; charset=us-ascii",
        "DKIM-Signature": "v=1; a=rsa-sha256; c=relaxed/relaxed; d=comcast.net;\n\ts=q20140121; t=1467724082;\n\tbh=+4noOLzzrCDUMpdmYJUqt/JMcTXlHPAr2vhKyFryBUY=;\n\th=Received:Received:From:Content-Type:Subject:Message-Id:Date:To:\n\t Mime-Version;\n\tb=jlfQ9jFzyv9EP/ioD4B3TgJF7U3S60MygklSXCmpSftTp78gxYY502XgMsV5WAYaK\n\t t9a2O7Hssmbfi5U+rZ8R0hhtFqDyfsbE6xxUvfHvSyHAjJ7XISwxQnvEJ/EhLeN3G7\n\t Ht/mIz9uim8atrnxSaZDyO09t5JoM70aPFBmbTSE9+3bWJDi8M/Apvsj/q+Zu1jHJ1\n\t buxk9iitgmFegKUfSktydc6tFE4y8yObF41n4EAHC2uuURPbtXwWHWRH/nap4sK/aI\n\t FwIMTEbbNyEC0/wEqy0dktUYX2pnakh8DdH+TX34ozKKr9exGAFYwgoGQEvnPAhRJi\n\t FdxJf5QfRfMeg==",
        "Date": "Tue, 5 Jul 2016 09:08:01 -0400",
        "Delivered-To": "moderator for announce@httpd.apache.org",
        "From": "Jim Jagielski <jim@apache.org>",
        "List-Id": "<announce.httpd.apache.org>",
        "List-Post": "<mailto:announce@httpd.apache.org>",
        "Mailing-List": "contact announce-help@httpd.apache.org; run by ezmlm",
        ...
        "body": {
            "plain": "\n          Apache HTTP Server 2.4.23 Released\n\nThe Apache Software Foundation and the Apache HTTP Server Project\nare pleased to announce the release of version 2.4.23 of the Apache\nHTTP Server (\"Apache\"). 
            ...
...
```

We can see the usual structure of a Perceval JSON document, with some metainformation (such as `backend_name`), and all the content the corresponding message in the `data` field. The structure of that content is one field per header, with the same name the header has in the message. For the body of the message, the field `body` is used.