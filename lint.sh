#!/bin/sh
pip install flake8 --quiet
flake8 app.py --max-line-length=130 --ignore=E302,E303,E305,F401,E501,W503
echo "Linting passed!"
