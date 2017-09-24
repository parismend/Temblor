cd /home/mekler/Documents/Temblor/etls/googlesheets/crowdsourced
source /home/ubuntu/secrets.sh
echo "corremos todo sobre pyenv local 3.6.1"
PATH=$PATH:/home/ubuntu/google-cloud-sdk/bin
export PATH
source /home/ubuntu/secrets.sh

export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
echo $PATH

fecha=`date +%s`

echo "esta por comenzar todo.....chan chaaaaan!!!"
python3 crowdsourcing.py
# python limpieza.py
echo 'Se generó datos_crowdsourced.csv'

echo "Vamos a subir todo a google"
gsutil -m cp datos_crowdsourced.csv gs://sismocdmx/datos_crowdsourced/
gsutil -m cp datos_crowdsourced.csv gs://sismocdmx/datos_crowdsourced/datos_crowdsourced$fecha.csv
gsutil acl ch -u AllUsers:R gs://sismocdmx/datos_crowdsourced/datos_crowdsourced.csv
bq load --replace --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.datos_crowdsourced gs://sismocdmx/datos_crowdsourced/datos_crowdsourced.csv

echo "eliminamos archivo local y terminamos"
rm datos_crowdsourced.csv
