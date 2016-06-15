from nose.tools import *
import unittest
import os
import sys

curr_path = os.path.abspath("__main__")
print(curr_path)
previous_folder = "/".join(curr_path.split('/')[:-2])
sys.path.append(previous_folder)
print(previous_folder)
from poller import *

class WebPollerTester(unittest.TestCase):

    def test_logger_webpoller_factory(self):
        """ TODO """
        pass

    def test_check_settings_sections(self):
        """ TODO """
        pass

    def test_time_decorator(self):
        """ TODO """
        pass

    def test_get_html(self):
        """ TODO """
        pass

    def test_check_rule_output(self):
        """ TODO """
        pass

    def test_WebPoller_create(self):
        """ TODO """
        pass

    def test_WebPoller_run(self):
        """ TODO """
        pass

    def test_WebPoller_logger(self):
        """ TODO """
        pass


if __name__ == '__main__':
    unittest.main()
