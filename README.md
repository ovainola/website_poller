[![Build Status](https://travis-ci.org/ovainola/website_poller.svg?branch=master)](https://travis-ci.org/ovainola/website_poller)


## WebPoller

A small implementation of a program that monitors web sites and reports their
availability. This tool is intended as a monitoring tool for web site
administrators for detecting problems on their sites.

The program has a browser interface, which is created via [pyramid](http://www.pylonsproject.org/). The python class, which polls
for sites and their availability has following dependencies:

 * requests
 * pyramid

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
defines the interval, in which the pages are polled. Pages defines a json file,
where the urls and rules for given sites are defined. In the logging section there is one keyword: settings. Settings defines a settings file for logging. For more informations for ConfigParser, check out [for python 2.7](https://docs.python.org/2/library/configparser.html) and [for python 3.5](https://docs.python.org/3.5/library/configparser.html) and for logging settings file [for python 2.7](https://docs.python.org/2/library/logging.config.html) and
[for python 3.5](https://docs.python.org/3.5/library/logging.config.html). The poll_pages.json file has a following structure:


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

Sites and urls as keywords are obvious, but in the rules, there are some things
to note. When a html site is fetched using requests, rules are applied to that page
to check the content. As seen above, "__contains__" and "__len__" are string methods,
and used as keywords here. Values for these keywords are list of lists, in which
are the arguments. For example, in "__len__" keyword, there is only one list
inside a list: ["None", 125]. The first element is the string method argument and
the second is the expected value. In the implementation html pages is stored as strings.
Hooks to string functions, f.ex. "__len__", to the html strings are got with getattr -function. When a hook to a string method is created, arguments are passed into
this method, f.ex. in the case of "__contains__": "foo" and "bar". Then the
output is check using equality operator with second argument, f.ex. in the case of "__contains__": "True" and "False". Output is a list of booleans, which
again are printed in the log file.
