#!/bin/bash
echo 'Corriendo daños colab'
python googlesheets.py
echo 'Corriendo daños internos'
python bici_squad.py
echo 'Pegando'
python pullcdb2.py
echo 'Se generó danios.csv'
python albergues.py
echo 'Se generó albergue.csv'
