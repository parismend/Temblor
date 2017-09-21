cd /home/ubuntu/Temblor/etls
export HOME=/home/ubuntu
#PATH=$PATH:/usr/local/bin
PATH=$PATH:/home/ubuntu/.pyenv/shims/
export PATH
echo $PATH

fecha=`date +%s`

python --version > /home/ubuntu/version
echo "esta por comenzar todo.....chan chaaaaan!!!"
python googlesheets/danios/googlesheets.py

echo "renombramos archivos"
mv datos.csv danios$fecha.csv
cp danios$fecha.csv danios.csv

cd
echo "Vamos a subir todo a google"
./gdrive upload --delete -p 0BxE-J-cXPDSDUzRBNDI4eUN3UGs Temblor/etls/danios$fecha.csv

echo "subimos la copia"
./gdrive upload --delete -p 0ByAjybdB6DdxOUxfYm9fbDdaNlU Temblor/etls/danios.csv
echo "termino..."
