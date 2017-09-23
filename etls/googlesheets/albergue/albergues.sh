cd /home/ubuntu/Temblor/etls/googlesheets/albergue
echo "corremos todo sobre pyenv local 3.6.1"
PATH=$PATH:/home/ubuntu/google-cloud-sdk/bin
export PATH
export HOME=/home/ubuntu


export GOOGLE_API_KEY="AIzaSyA5kS3WYhJVYy7k9eZr3YfP8BE8l_A8eP0"
export GM_KEY="AIzaSyA5kS3WYhJVYy7k9eZr3YfP8BE8l_A8eP0"

#PATH=$PATH:/usr/local/bin
echo $PATH

fecha=`date +%s`
echo "esta por comenzar todo.....chan chaaaaan!!! asdfasdfa"
python3 albergues.py


echo "va el path"
echo $PATH
echo "cambiamos a python 2.7.12 para poder usar gcloud entonces....carpeta puerca"

echo "Vamos a subir todo a google"
gsutil -m cp albergues.csv gs://sismocdmx/albergues/
gsutil -m cp albergues.csv gs://sismocdmx/albergues/albergues$fecha.csv
gsutil acl ch -u AllUsers:R gs://sismocdmx/albergues/albergues.csv
bq load --replace --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.albergues gs://sismocdmx/albergues/albergues.csv

echo "eliminamos archivo local y terminamos"
rm albergues.csv
