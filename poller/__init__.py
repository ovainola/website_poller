import sys
if sys.version_info.major == 3:
    from .WebPoller import WebPoller, logger_webpoller_factory
    from .WebPoller import get_html, _rule_mapper, check_rule_output
else:
    from WebPoller import WebPoller, logger_webpoller_factory
    from WebPoller import get_html, _rule_mapper, check_rule_output
