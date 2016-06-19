import logging
from logging.config import fileConfig
import ConfigParser
import json
import numpy as np
import os
import time
from poller import *


if __name__ == "__main__":
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
