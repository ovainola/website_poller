import requests
import threading
import time
import logging
import json
import sys
from logging.config import fileConfig
import ConfigParser
import os

# All the official connection types
# See https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
CONNECTION_TYPES = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information (since HTTP/1.1)",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content (RFC 7233)",
    207: "Multi-Status (WebDAV; RFC 4918)",
    208: "Already Reported (WebDAV; RFC 5842)",
    226: "IM Used (RFC 3229)",
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other (since HTTP/1.1)",
    304: "Not Modified (RFC 7232)",
    305: "Use Proxy (since HTTP/1.1)",
    306: "Switch Proxy",
    307: "Temporary Redirect (since HTTP/1.1)",
    308: "Permanent Redirect (RFC 7538)",
    400: "Bad Request",
    401: "Unauthorized (RFC 7235)",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required (RFC 7235)",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed (RFC 7232)",
    413: "Payload Too Large (RFC 7231)",
    414: "URI Too Long (RFC 7231)",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable (RFC 7233)",
    417: "Expectation Failed",
    418: "I'm a teapot (RFC 2324)",
    421: "Misdirected Request (RFC 7540)",
    422: "Unprocessable Entity (WebDAV; RFC 4918)",
    423: "Locked (WebDAV; RFC 4918)",
    424: "Failed Dependency (WebDAV; RFC 4918)",
    426: "Upgrade Required",
    428: "Precondition Required (RFC 6585)",
    429: "Too Many Requests (RFC 6585)",
    431: "Request Header Fields Too Large (RFC 6585)",
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates (RFC 2295)",
    507: "Insufficient Storage (WebDAV; RFC 4918)",
    508: "Loop Detected (WebDAV; RFC 5842)",
    510: "Not Extended (RFC 2774)",
    511: "Network Authentication Required (RFC 6585)"
}

def logger_webpoller_factory(settings_file, sections):
    """
    """
    # Create config parser and read configs
    config = ConfigParser.ConfigParser()
    vals = config.read(settings_file)
    if len(vals) == 0:
        raise IOError("Given settings file is empty. Please check the settings file's path.")

    check_settings_sections(config, sections)

    time_period = config.get("main", "time_period")
    logging_settings = config.get("logging", "settings")

    # Store both settings and logging files paths for checking mod.date
    loggins_settings_path = os.path.abspath(logging_settings)
    settings_abs_path = os.path.abspath(settings_file)

    fileConfig(logging_settings)
    main_logger = logging.getLogger("Server")
    web_logger = logging.getLogger("WebPoller")

    page_file = config.get("main", "pages")
    with open(page_file, "r") as f:
        page_data = json.load(f)

    webpoller = WebPoller(page_data["pages"], time_period, logger=web_logger)
    return webpoller, main_logger

def check_settings_sections(config, necessary_sections):
    """
    """
    keys = necessary_sections.keys()
    if not all([x in necessary_sections.keys() for x in config.sections()]):
        raise ValueError("Not all section present in settings. Necessary sections names: %s" % ", ".join(*keys))

    for each in keys:
        sections = necessary_sections[each]
        section_names = [x[0] for x in config.items(each)]
        if not all([x in sections for x in section_names]):
            raise ValueError("Not all {0} section items present in settings. Necessary {0} sections items:".format(each) +
                             " ,".join(*sections) )

def time_decorator(func):
    """Decorator, for clocking the response time

    Parameters
    ----------
    func: function
        Function, which is decorated
    """
    def class_method_deco(*args):
        """
        Inner function of decorator

        Parameters
        ----------
        args: list
            List of arguments passed into the function
        """
        start = time.time()
        vals = func(*args)
        stop = time.time()
        spent_time = stop - start
        return vals, spent_time
    return class_method_deco

@time_decorator
def get_html(url, logger=None):
    """Fetches url using requests package.

    Parameters
    ----------
    url: string
        Url, of the interest

    Returns
    -------
    Dictionary
        Response dict. Dict has following keys:
            connected: Boolean
                request was successful
            obj: Response object
                If connection successful, obj contains the data from requests
            status_code: list
                list, in which: index 0 is the connection details,
                                index 1 is the connection code
    """
    res = {}
    try:
        response = requests.get(url)
        status_code = response.status_code
        res["status_code"] = [CONNECTION_TYPES.get(status_code, "Not implemented"),
                              status_code]
        res["obj"] = response
        res["connected"] = True
    except requests.exceptions.ConnectionError as err:
        if logger != None:
            logger.error(err)
        else:
            print(err)
        res["connected"] = False
        res["obj"] = None
        res["status_code"] = [None, None]
    return res


def check_rule_output(rules, resp_as_text):
    """Checks if given string contains the defined rules

    Parameters
    ----------
        rules: Dict
            Dictionary of the rules. In rules keys are string methods and
            values are lists in list. Rules has to have following structure:
            >> rules =  {"__contains__": [["Oulun", "True"]],
                         "count":  [["not found", "0"]]}}
        resp_as_text: string
            String, in which the rules are applied

    Returns
    -------
        Dictionary
            Dictionary, in which keys are string method names and
            values are boolean lists
    """
    expected_values = {}
    for method, expected in rules.items():
        method_hook = getattr(resp_as_text, method)
        expected_values[method] = map(lambda inp: str(str(method_hook(inp[0])) == inp[1]), expected)
    return expected_values


class WebPoller(threading.Thread):
    """ Website poller

    Implementation of a program that monitors web sites and reports their
    availability. This tool is intended as a monitoring tool for web site
    administrators for detecting problems on their sites.
    """

    def __init__(self, poll_sites, period_time, logger=None):
        """Constructor

        Parameters
        ----------
            poll_sites: dict
                Dictionary of the polling sites. Dict has to have following structure:
                >> poll_sites = {"http://foobar.com": {
                                "rules":
                                    {"__contains__": ["google", "True"]}
                                },
                            "http://another_test.com": {
                                            "rules":
                                                {"__contains__": ["flox", "True"],
                                                 "count": ["flux", "12"]}
                                            },
                            }
            period_time: int of float
                The periodical time, when the sites are fetched
            logger: None or logging.getLogger
                Logger for logging purposes
        """
        threading.Thread.__init__(self)
        self.poll_sites = poll_sites
        self.period_time = float(period_time)
        self._init_status_dict()
        self._init_logger(logger)

    def _init_logger(self, logger):
        """Initialize logger
        """
        if logger == None:
            self.logger = logging.getLogger("WebPoller")
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                    '%(asctime)s %(name) %(levelname) %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        else:
            self.logger = logger

    def _init_status_dict(self):
        """Initialize polling dictionary, in which the results are stored
        """
        self.poll_dict = {}
        for each in self.poll_sites.items():
            url, vals = each
            self.poll_dict[url] = {}
            self.poll_dict[url]["status_code"]   = -1
            self.poll_dict[url]["response_time"] = -1
            self.poll_dict[url]["rule_output"]   = []
            self.poll_dict[url]["connected"]     = "False"

    def run(self):
        """Thread function

        This is the async function, in which the sites are gathered and processed
        """
        while True:
            for each in self.poll_sites.items():
                url, vals = each
                response, resp_time = get_html(url, self.logger)

                # If was able to connect to server
                if response["connected"]:
                    rules = vals["rules"]
                    resp_obj = response["obj"]
                    resp_as_text = resp_obj.text
                    rule_output = check_rule_output(rules, resp_as_text)
                    status_code_list = response["status_code"]
                else:
                    rule_output = []

                # Update values to poll dictionary
                self.poll_dict[url]["status_code"]   = response["status_code"]
                self.poll_dict[url]["response_time"] = resp_time
                self.poll_dict[url]["rule_output"]   = rule_output
                self.poll_dict[url]["connected"]     = str(response["connected"])

                # Print output to log
                self.logger.info("Fetching {0}:".format(url))
                self.logger.info(" *** Response time: {0:.3f} seconds.".format(resp_time))
                self.logger.info(" *** Status: {0}, code: {1}.".format(*status_code_list))
                for rule_name, list_vals in rule_output.items():
                    self.logger.info(" *** Rule: {0}, output: {1}".format(
                        rule_name, ", ".join(list_vals)))

            self.logger.info(" ---- Sleeping {0} seconds ---- ".format(str(self.period_time)))
            time.sleep(self.period_time)

    def change_poll_pages(self, json_pages):
        """ Change the sites, which are polled

        Parameters
        ----------
        json_pages: Dict
            Dictionary of pages. Here is an example format:
            >> pages = {"http://foobar.com": {
                            "rules":
                                {"__contains__": ["foobar", "True"]}
                            },
                        "http://foobaz.com": {
                                        "rules":
                                            {"__contains__": ["flux", "True"],
                                             "count": ["flox", "12"]}
                                        },
                        }
        """
        self.poll_sites = json_pages
        self._init_status_dict()

    def change_period_time(self, new_period_time):
        """ Change the period time for polling the pages

        Parameters
        ----------
        new_period_time: int or float
            New period time
        """
        self.period_time = new_period_time

    def poll_results(self):
        """Returns the results from recent poll

        Returns
        -------
        Dict
            Values of the recent poll
        """
        return self.poll_dict



if __name__ == "__main__":
    # this if part is mainly for testing WebPoller on solo
    import logging
    from logging.config import fileConfig
    import ConfigParser
    import json
    import numpy as np
    import os
    import time

    filepath = os.path.abspath("__main__")
    previous_folder = "/".join(np.array(filepath.split("/"))[:-2])
    os.chdir(previous_folder)
    settings = "settings.conf"

    config = ConfigParser.ConfigParser()
    config.read(settings)

    period_time = config.get("main", "time_period")
    logging_settings = config.get("logging", "settings")
    fileConfig(logging_settings)
    logger = logging.getLogger("webpoller")

    page_file = config.get("main", "pages")
    with open(page_file, "r") as f:
        page_data = json.load(f)

    webpoller = WebPoller(page_data["pages"], period_time, logger=logger)
    webpoller.start()