cd /home/ubuntu/Temblor/etls
export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
PATH=$PATH:/home/ubuntu/.pyenv/shims/
export PATH
echo $PATH

fecha=`date +%s`

python --version > /home/ubuntu/version
echo "esta por comenzar todo.....chan chaaaaan!!!"
python googlesheets/albergue/albergues.py

echo "renombramos archivos"
mv albergues.csv albergues$fecha.csv
cp albergues$fecha.csv albergues.csv

cd
echo "Vamos a subir todo a google"
./gdrive upload --delete -p 0BxE-J-cXPDSDUzRBNDI4eUN3UGs Temblor/etls/albergues$fecha.csv

echo "subimos la copia"
./gdrive upload --delete -p 0ByAjybdB6DdxOUxfYm9fbDdaNlU Temblor/etls/albergues.csv
echo "termino..."
