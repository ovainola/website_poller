import sys
if sys.version_info.major == 3:
    from .WebPoller import WebPoller, logger_webpoller_factory, check_settings_sections
    from .WebPoller import get_html, _rule_mapper, check_rule_output, EXCEPTED_SECTIONS
    from .WebPoller import _time_decorator
else:
    from WebPoller import WebPoller, logger_webpoller_factory, check_settings_sections
    from WebPoller import get_html, _rule_mapper, check_rule_output, EXCEPTED_SECTIONS
    from WebPoller import _time_decorator
