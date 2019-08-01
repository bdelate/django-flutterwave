"""
Add project base path to sys path. This allows jupyter notebooks to reside
in the jupyter_notebook sub directory (as per notebook-dir in settings) but
allows for clean imports as if jupyter is running from the project root.
"""
import sys
import os

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_BASE_PATH = os.path.abspath(os.path.join(FILE_PATH, ".."))

sys.path.insert(1, PROJECT_BASE_PATH)
