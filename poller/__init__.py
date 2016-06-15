import sys
if sys.version_info.major == 3:
    from .WebPoller import WebPoller, logger_webpoller_factory
else:
    from WebPoller import WebPoller, logger_webpoller_factory
