cd /home/ubuntu/Temblor/etls/googlesheets/acopio
source /home/ubuntu/secrets.sh
echo "corremos todo sobre pyenv local 3.6.1"
PATH=$PATH:/home/ubuntu/google-cloud-sdk/bin
export PATH
export PATH_MANZANAS=/home/ubuntu/Temblor/datos/manzanas_inegi/man*.shp
export PATH_DANIOS=/home/ubuntu/Temblor/etls/googlesheets/acopio/acopio.csv
source /home/ubuntu/secrets.sh

export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
echo $PATH

fecha=`date +%s`

echo "esta por comenzar todo.....chan chaaaaan!!!"
python3 acopios.py
# python limpieza.py
echo 'Se generó acopio.csv'

echo "Vamos a subir todo a google"
gsutil -m cp acopio.csv gs://sismocdmx/acopio/
gsutil -m cp acopio.csv gs://sismocdmx/acopio/acopio$fecha.csv
gsutil acl ch -u AllUsers:R gs://sismocdmx/acopio/acopio.csv
bq load --replace --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.acopio gs://sismocdmx/acopio/acopio.csv

echo "eliminamos archivo local y terminamos"
rm acopio.csv datos.csv bici_squad.csv
