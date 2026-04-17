import os
import sys

# Ensure the package in 1.pomodoro is importable as 'pomodoro' during tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
POM_DIR = os.path.join(ROOT, '1.pomodoro')
if POM_DIR not in sys.path:
    sys.path.insert(0, POM_DIR)
