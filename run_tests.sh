#!/bin/sh
pip install selenium --quiet
apt-get update -qq
apt-get install -y -qq chromium chromium-driver
python /tests/test_selenium.py
