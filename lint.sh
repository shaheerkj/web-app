#!/bin/sh
pip install flake8 --quiet
flake8 app.py --max-line-length=120
