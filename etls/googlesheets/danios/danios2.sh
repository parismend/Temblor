cd /home/ubuntu/Temblor/etls/googlesheets/danios
echo "corremos todo sobre pyenv local 3.6.1"
PATH=$PATH:/home/ubuntu/.pyenv/shims/:/home/ubuntu/.pyenv/bin/:/home/ubuntu/google-cloud-sdk/bin
export PATH
export PATH_MANZANAS=/home/ubuntu/Temblor/datos/manzanas_inegi/man*.shp
export PATH_DANIOS=/home/ubuntu/Temblor/etls/googlesheets/danios/danios.csv
source /home/ubuntu/secrets.sh

pyenv local 3.6.1

export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
echo $PATH

fecha=`date +%s`
echo pwd
echo "esta por comenzar todo.....chan chaaaaan!!!"
python googlesheets.py
python bici_squad.py
python pullcdb2.py
python limpieza.py
echo 'Se generó danios.csv'

echo "cambiamos a python 2.7.12 para poder usar gcloud"
pyenv local 2.7.12

echo "Vamos a subir todo a google"
gsutil -m cp danios_clean.csv gs://sismocdmx/danios/danios_clean.csv
# gsutil -m cp danios_clean.csv gs://sismocdmx/danios/danios_clean$fecha.csv
# bq load --replace --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.danios gs://sismocdmx/danios/danios.csv

echo "eliminamos archivo local y terminamos"
# rm danios_clean.csv danios.csv datos.csv bici_squad.csv
