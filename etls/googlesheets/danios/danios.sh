cd /home/ubuntu/Temblor/etls/googlesheets/danios
source /home/ubuntu/secrets.sh
echo "corremos todo sobre pyenv local 3.6.1"
PATH=$PATH:/home/ubuntu/google-cloud-sdk/bin
export PATH
export PATH_MANZANAS=/home/ubuntu/Temblor/datos/manzanas_inegi/man*.shp
export PATH_DANIOS=/home/ubuntu/Temblor/etls/googlesheets/danios/danios.csv
source /home/ubuntu/secrets.sh

export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
echo $PATH

fecha=`date +%s`

echo "esta por comenzar todo.....chan chaaaaan!!!"
python3 googlesheets.py
python3 bici_squad.py
python3 pullcdb2.py
# python limpieza.py
echo 'Se generó danios.csv'

echo "Vamos a subir todo a google"
gsutil -m cp danios.csv gs://sismocdmx/danios/
gsutil -m cp danios.csv gs://sismocdmx/danios/danios$fecha.csv
gsutil acl ch -u AllUsers:R gs://sismocdmx/danios/danios.csv
bq load --replace --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.danios gs://sismocdmx/danios/danios.csv

echo "eliminamos archivo local y terminamos"
rm danios.csv datos.csv bici_squad.csv