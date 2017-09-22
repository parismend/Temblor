cd /home/ubuntu/Temblor/etls
echo "corremos todo sobre pyenv local 3.6.1"
PATH=$PATH:/home/ubuntu/.pyenv/shims/:/home/ubuntu/.pyenv/bin/:/home/ubuntu/google-cloud-sdk/bin
export PATH

pyenv local 3.6.1

export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
echo $PATH

fecha=`date +%s`

python --version > /home/ubuntu/version
echo "esta por comenzar todo.....chan chaaaaan!!!"
python googlesheets/danios/googlesheets.py
python googlesheets/danios/bici_squad.py
python googlesheets/danios/pullcdb2.py
echo 'Se generó danios.csv'

echo "cambiamos a python 2.7.12 para poder usar gcloud"
pyenv local 2.7.12

echo "Vamos a subir todo a google"
gsutil -m cp danios.csv gs://sismocdmx/danios/
gsutil -m cp danios.csv gs://sismocdmx/danios/danios$fecha.csv
bq load --replace --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.danios gs://sismocdmx/danios/danios.csv

echo "eliminamos archivo local y terminamos"
rm danios.csv datos.csv bici_squad.csv