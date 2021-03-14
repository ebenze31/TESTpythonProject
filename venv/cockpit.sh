#!/bin/bash
cd /var/www/viicheck.com/TESTpythonProject/venv/
source Scripts/activate
cd scraping_cockpit/
python3 cockpit.py
deactivate