"""Test configuration for module tests."""

import os
import sys

# Add the tests directory to the path to import conftest.py
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../tests"))
sys.path.insert(0, tests_dir)

# Import all fixtures from the main conftest.py
from conftest import *
