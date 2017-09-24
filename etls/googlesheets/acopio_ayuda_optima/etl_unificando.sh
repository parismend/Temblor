cd /home/ubuntu/Temblor/etls/googlesheets/acopio_ayuda_optima
source /home/ubuntu/secrets.sh
echo "corremos todo sobre pyenv local 3.6.1"
PATH=$PATH:/home/ubuntu/google-cloud-sdk/bin
export PATH
export PATH_MANZANAS=/home/ubuntu/Temblor/datos/manzanas_inegi/man*.shp
export PATH_ACOPIO_AYUDA_OPTIMA=/home/ubuntu/Temblor/etls/googlesheets/acopio_ayuda_optima/acopio_ayuda_optima.csv
source /home/ubuntu/secrets.sh

export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
echo $PATH

fecha=`date +%s`

echo "esta por comenzar harvard mit etl.....chan chaaaaan!!!"
python3 etl_unificando.py
# python limpieza.py
echo 'Se generó acopio_ayuda_optima.csv'

echo "Vamos a subir todo a google"
gsutil -m cp harvard_mit.csv gs://sismocdmx/acopio-ayuda-optima/
gsutil -m cp harvard_mit.csv gs://sismocdmx/acopio-ayuda-optima/acopio_ayuda_optima$fecha.csv
gsutil acl ch -u AllUsers:R gs://sismocdmx/acopio-ayuda-optima/acopio_ayuda_optima.csv
bq load --replace --autodetect --source_format CSV --skip_leading_rows 1 sismocdmx.harvard-mit gs://sismocdmx/acopio-ayuda-optima/acopio_ayuda_optima.csv

echo "eliminamos archivo local y terminamos"
rm acopio_ayuda_optima.csv
