from nose.tools import *
import os
import sys

curr_path = os.path.abspath("__main__")
print(curr_path)
previous_folder = "/".join(curr_path.split('/')[:-2])
sys.path.append(previous_folder)
print(previous_folder)
from poller import *
