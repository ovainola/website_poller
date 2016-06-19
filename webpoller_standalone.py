import logging
from logging.config import fileConfig
import ConfigParser
import json
import numpy as np
import os
import time
from poller import *


if __name__ == "__main__":
    webpoller, logger = logger_webpoller_factory("settings.conf")
    webpoller.start()
