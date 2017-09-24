cd /home/ubuntu/Temblor/etls/googlesheets/harvard_mit
source /home/ubuntu/secrets.sh
echo "corremos todo sobre pyenv local 3.6.1"
PATH=$PATH:/home/ubuntu/google-cloud-sdk/bin
export PATH
export PATH_MANZANAS=/home/ubuntu/Temblor/datos/manzanas_inegi/man*.shp
export PATH_HARVARD_MIT=/home/ubuntu/Temblor/etls/googlesheets/harvard_mit/harvard_mit.csv
source /home/ubuntu/secrets.sh

export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
echo $PATH

fecha=`date +%s`

echo "esta por comenzar harvard mit etl.....chan chaaaaan!!!"
python3 Base_H_MIT.py
# python limpieza.py
echo 'Se generó harvard_mit.csv'

echo "Vamos a subir todo a google"
gsutil -m cp harvard_mit.csv gs://sismocdmx/harvard-mit/
gsutil -m cp harvard_mit.csv gs://sismocdmx/harvard-mit/harvard_mit$fecha.csv
gsutil acl ch -u AllUsers:R gs://sismocdmx/harvard-mit/harvard_mit.csv
bq load --replace --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.harvard_mit gs://sismocdmx/harvard-mit/harvard_mit.csv

echo "eliminamos archivo local y terminamos"
rm harvard_mit.csv
