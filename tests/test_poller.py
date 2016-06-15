from nose.tools import *
import os
import sys
curr_path = os.path.abspath("__main__")
previous_folder = "/".join(curr_path.split('/')[:-2])
sys.path.append(previous_folder)
from poller import *
