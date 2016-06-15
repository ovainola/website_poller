[![Build Status](https://travis-ci.org/ovainola/website_poller.svg?branch=master)](https://travis-ci.org/ovainola/website_poller)


## WebPoller

A small implementation of a program that monitors web sites and reports their
availability. This tool is intended as a monitoring tool for web site
administrators for detecting problems on their sites.

The program has a browser interface, which is created via [pyramid](http://www.pylonsproject.org/). The python class, which polls
for sites and their availability is created using requests & threading.
