[![Build Status](https://travis-ci.org/ovainola/website_poller.svg?branch=master)](https://travis-ci.org/ovainola/website_poller)

[![Coverage Status](https://coveralls.io/repos/github/ovainola/website_poller/badge.svg?branch=master)](https://coveralls.io/github/ovainola/website_poller?branch=master)


# WebPoller

An implementation of a program that monitors web sites and reports their
availability. This tool is intended as a monitoring tool for web site
administrators for detecting problems on their sites.

The program has has following dependencies:

 * [requests](http://docs.python-requests.org/en/master/)
 * [flask](http://flask.pocoo.org/)


### How it works

 Web application uses ConfigParser to read the settings.conf file for necessary
 information. The settings.conf has a following structure:

 ```
 [main]
 time_period: 60
 pages: poll_pages.json

 [logging]
 settings: logging_settings.ini
 ```

In the main section, there are two keywords: time_period and pages. Time_period
defines the interval the pages are polled. Pages -keyword defines a json file,
where the interested urls and rules are defined. In the logging section
there is one keyword: settings. Settings defines a settings file for logging.
For more informations for ConfigParser, check out [for python 2.7](https://docs.python.org/2/library/configparser.html)
and [for python 3.5](https://docs.python.org/3.5/library/configparser.html)
and for logging settings file [for python 2.7](https://docs.python.org/2/library/logging.config.html) and
[for python 3.5](https://docs.python.org/3.5/library/logging.config.html).
The poll_pages.json file has a following structure:

```
{
  "pages": {
    "https://foobar.com/": {
      "rules": {
        "__contains__": [["foo", "True"], ["bar", "False"]],
        "__len__": [["None", 125]]}
      },
    "https://foobaz.com/": {
      "rules": {
        "find": [["baz", 27]]}
    },
  }
}
```

Using urls as keywords is pretty obvious, but for the rules, there are some things
to note. When a html site is fetched using requests, rules are applied to that page
to check the content. As seen above, "\__contains__" and "\__len__" are string methods,
and used as keywords here. Values for these keywords are list of lists. In the inner list
are the arguments. For example, in "\__len__" keyword, there is only one list
inside a list: ["None", 125]. The first element is the string method's argument and
the second is the expected value. In the implementation html pages are stored as strings.
Hooks to string functions, f.ex. "\__len__", to the html strings are got with getattr -function.
When a hook to a string method is created, arguments are passed into
this method, f.ex. in the case of "\__contains__", "foo" is passed into the method hook
and the output is checked using equality operator to check if it's a match with second argument, "bar".
When all the rule arguments are tested function returns a list of booleans.

In the logfile are printed urls, response times, status of the request
(code and details) and output of the rules.

### How do I use it?

 Clone it, install requirements, change settings and apply:

 ```
 python app.py
 ```

and open your favorite browser and apply url http://localhost:5000. If you want to
run without browser interface:

```
python webpoller_standalone.py
```
