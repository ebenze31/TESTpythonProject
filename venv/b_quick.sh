#!/bin/bash
cd /var/www/viicheck.com/TESTpythonProject/venv/
source Scripts/activate
cd scraping\ one2car/
python3 scraping.py
deactivate