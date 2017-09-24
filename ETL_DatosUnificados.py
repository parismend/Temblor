import pandas as pd
import numpy as np

datos = pd.read_csv('/Users/alejandronivon/Desktop/ETL/UNIFICANDO CENTROS DE AYUDA')
datos.columns=datos.loc[5,]
datos=datos.loc[6:,]

datos=datos[['DESCRIPCIÓN', 'DELEGACIÓN/ENTIDAD FEDERATIVA ', 'COLONIA ', 'Lugar de REFERENCIA',
	'DIRECCIÓN', 'HORARIOS DE ATENCIÓN', 'REQ TRANSPORTE PARA MOVER VÍVERES A OTRO LUGAR', 
	 'Mandan víveres hacia ', 'Horarios de salidas', 'NECESITAN', 'OFRECEN VÍVERES A QUIEN LO NECESITEN', 
	 's19 POR FAVOR NO MODIFICAR', 'FECHAS 19s', 'LAT ', 'LONG ']]

datos.columns=['DESCRIPCION', 'ENTIDADFEDERATIVA', 'COLONIA', 'LugardeREFERENCIA', 'DIRECCION', 
	'HORARIOSDEATENCION', 'REQTRANSPORTEPARAMOVERVIVERESAOTROLUGAR', 'Mandanvivereshacia', 
	'Horariosdesalida', 'NECESITAN', 'ESCESODEVIVERES', 
	'S19NoModificar', 'FECHAS19s', 'LAT', 'LONG']

datos = datos.loc[datos['S19NoModificar'] == '1']
datos = datos.loc[-(datos['Lat'].isnull()) & -(datos['Long'].isnull())]

del datos['S19NoModificar']

print(datos.head())