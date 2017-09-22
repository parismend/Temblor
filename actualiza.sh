#!/bin/bash
python googlesheets.py
python bici_squad.py
python pullcdb2.py
echo 'Se generó danios.csv'
python albergues.py
echo 'Se generó albergue.csv'
