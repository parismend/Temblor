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
python googlesheets/albergue/albergues.py

echo "cambiamos a python 2.7.12 para poder usar gcloud"
pyenv local 2.7.12

echo "Vamos a subir todo a google"
gsutil -m cp albergues.csv gs://sismocdmx/albergues/
gsutil -m cp albergues.csv gs://sismocdmx/albergues/albergues$fecha.csv
bq load --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.albergues gs://sismocdmx/albergues/albergues.csv

echo "eliminamos archivo local y terminamos"
rm albergues.csv
