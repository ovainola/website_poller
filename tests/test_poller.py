from nose.tools import *
import unittest
import os
import sys
import numpy as np

curr_path = os.path.abspath("__main__")
print(curr_path)
previous_folder = "/".join(curr_path.split('/')[:-2])
sys.path.append(previous_folder)
print(previous_folder)
from poller import *
import poller

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

    def test_get_html_200(self):
        """ Test for successfully fetching a html page with code 200"""
        url = "http://google.fi"
        response, rtime = get_html(url)
        self.assertTrue(response["connected"])
        self.assertTrue(response["status_code"][1] == 200)

    def test_get_html_404(self):
        """ Test for successfulle fetching a html page with 404 code """
        url = "http://httpbin.org/status/404"
        response, rtime = get_html(url)
        self.assertTrue(response["connected"])
        self.assertTrue(response["status_code"][1] == 404)

    def test_get_html_not_defined(self):
        """ Test for failing to fetch a html page """
        url = "http://thispagedoesnotexists.com"
        response, rtime = get_html(url)
        self.assertTrue(response["connected"] == False)
        self.assertTrue(response["status_code"][1] == None)

    def test_get_html_not_defined_2(self):
        """ Test for failing to fetch a html page """
        url = "gibberish dibberig"
        response, rtime = get_html(url)
        self.assertTrue(response["connected"] == False)
        self.assertTrue(response["status_code"][1] == None)

    def test_rule_mapper(self):
        """ Test for string rule mapper """
        a = ["my test string", "my test string", "", "dippadaa"]
        method = ["__len__", "__contains__", "find", "__contains__"]
        args = ["None", "my", "my", "diu"]
        expected = [len(a), True, "True", "False"]
        for i in np.arange(len(a)):
            l_a = a[i]
            l_met = method[i]
            l_arg = args[i]
            l_exp = args[i]
            hook = getattr(l_a, l_met)
            val = poller._rule_mapper(hook, l_arg, l_exp)
            self.assertTrue(bool(val))

    def test_check_rule_output(self):
        """ tet for checking rule output """
        st = """
  </div><!-- /#dashboard -->
</div><!-- /.container -->fae
ae
      </div>
      <div class="moda</div>aef
    </div>

        <div class="contaegainer site-footer-container">
  <div class="site-footaeger" role="contentinfo">
    <ul class=aegag"site-footer-links right">

        <li><a githagaegub.com/blog" data">Bafeaeflofaeg</a></li>
        <li><a hFootaefer, go to about, text:about">Abaefaefaefaefout</a></li>

    </ul>aefaef

    <aaef hrfaefef="httaefaefps:ae//github.caefaefaefom" aria-label="Homeaefaepage" class=ffasitefae-footer-aefaefaeark" MYTITLE="GitHub">
        <li><a href=thub.com/site/terms" data-ga-click="Footer, eaeeafgo to terms, text:terms">Taefaeffaerms</a></li>
        <li><a href="htaefaeftps://gFooaefaefter, go to privacy, text:privacy">Privacy</a></li>
        <li><a href="httfaefaefps://github.coick="Footer, go to contact, text:contact">Contact</a></li>
        <li><a href="httpsaef://help.aefaefaefhelp">hHhdhteldthp<h/d</lhhhdi>
    </ul>
  </div>
</div>



    """
        rules = {"__contains__": [["Git", "True"], ["team", "False"]],
                 "find": [["Oulun", -1]]}

        bool_list = check_rule_output(rules, st)
        for name, vals in bool_list.items():
            orig_vals = rules[name]
            map(lambda x: self.assertTrue(bool(name[x]) == bool(orig_vals[x])), np.arange(len(orig_vals)))

    def test_init_WebPoller(self):
        """ Testing initializing WebPoller """
        pages = {"https://github.com/": {
                    "rules": {
                        "__contains__": [["Git", "True"], ["team", "True"]],
                        "find": [["Oulun", 125]]}
                    },
                "https://twitter.com/": {
                    "rules": {
                        "__contains__": [["twitter", "True"]]}
                    }
                }
        period_time = 120.
        webpoller

    def test_init_WebPoller(self):
        """ Testing initializing WebPoller """
        pages = { }
        period_time = "12e20."
        self.assertRaises(ValueError, WebPoller, pages, period_time)


if __name__ == '__main__':
    unittest.main()
