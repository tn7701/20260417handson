#!/usr/bin/env python3

import os
import sys


ROOT = os.path.dirname(__file__)
APP_DIR = os.path.join(ROOT, '1.pomodoro')
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from pomodoro import create_app  # noqa: E402


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
