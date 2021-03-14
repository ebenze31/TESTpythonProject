#!/bin/bash
cd /var/www/viicheck.com/TESTpythonProject/venv/
source Scripts/activate
cd scraping_b_quick/
python3 b_quick.py
deactivate