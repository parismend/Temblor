import pandas as pd
import requests
import re

ted = pd.read_csv('/Users/parismendez/Desktop/TED.csv')

urls = ted['Google Maps']
latitud = []
longitud = []
lat_lon = []
x = 0
while x < len(ted):
	try:
		url = urls[x]
		r = requests.head(url, allow_redirects=True)
		aaa = re.findall('(([0-9]*\.[0-9]+)[,]([-0-9]*\.[0-9]+))', r.url)
		lat_lon.append(aaa)
	except:
		lat_lon.append(aaa)
	x = x+1
y=0
while y < len(lat_lon):
	latitud.append(lat_lon[y][0][0].split(',')[0])
	longitud.append(lat_lon[y][0][0].split(',')[1])
	y = y+1
latitud = [lat_lon[x][0][0].split(',')[0] for x in lat_lon]
longitud = [lat_lon[x][0][0].split(',')[1] for x in lat_lon]


Delegacion = ted['Delegación']
Tipo_Infraestructura = ted['Lugar']
Tipo_del_Danio = ted['Tipo']
Hora_Reporte = ted['Última actualización (hr.)']
Viveres_Faltantes = ted['''#SeNecesita ''']

Calle = [''  for x in range(0,len(ted))]
Colonia = [''  for x in range(0,len(ted))]

Estado = [''  for x in range(0,len(ted))]
Foto = [''  for x in range(0,len(ted))]
Herramientas_Faltantes = [''  for x in range(0,len(ted))]
Herramientas_Sobrantes = [''  for x in range(0,len(ted))]
Hora = [''  for x in range(0,len(ted))]

Mano_Faltante = [''  for x in range(0,len(ted))]
Mano_Sobrantes = [''  for x in range(0,len(ted))]
Medicamentos_Faltantes = [''  for x in range(0,len(ted))]
Medicamentos_Sobrantes = [''  for x in range(0,len(ted))]
Numero_Exterior_Aproximado = [''  for x in range(0,len(ted))]
Numero_Personas_Atrapadas = [''  for x in range(0,len(ted))]
Numero_Personas_Desaparecidas = [''  for x in range(0,len(ted))]
Numero_Personas_Fallecidas = [''  for x in range(0,len(ted))]
Numero_Personas_Lesionadas = [''  for x in range(0,len(ted))]
Numero_Personas_Rescatadas = [''  for x in range(0,len(ted))]
Otra_Referencia_Ubicacion = [''  for x in range(0,len(ted))]
Timestamp = [''  for x in range(0,len(ted))]

Tipo_de_Uso = [''  for x in range(0,len(ted))]
Tipo_del_Danio = [''  for x in range(0,len(ted))]
Verificado = [''  for x in range(0,len(ted))]

Viveres_Sobrantes = [''  for x in range(0,len(ted))]



tedd = pd.DataFrame({
'Calle': Calle,
'Colonia': Colonia,
'Delegación': Delegacion,
'Estado' : Estado,
'Foto': Foto,
'Herramientas Faltantes': Herramientas_Faltantes,
'Herramientas Sobrantes': Herramientas_Sobrantes,
'Hora': Hora,
'Hora del Reporte': Hora_Reporte,
'Mano de Obra Faltante': Mano_Faltante,
'Mano de Obra Sobrantes': Mano_Sobrantes,
'Medicamentos Faltantes': Medicamentos_Faltantes,
'Medicamentos Sobrantes': Medicamentos_Sobrantes,
'Número Exterior  o Aproximado': Numero_Exterior_Aproximado,
'Número de Personas Atrapadas': Numero_Personas_Atrapadas,
'Número de Personas Desaparecidas': Numero_Personas_Desaparecidas,
'Número de Personas Fallecidas': Numero_Personas_Fallecidas,
'Número de Personas Lesionadas': Numero_Personas_Lesionadas,
'Número de Personas Rescatadas': Numero_Personas_Rescatadas,
'Otra Referencia de Ubicación ': Otra_Referencia_Ubicacion,
'Timestamp' : Timestamp,
'Tipo de Infraestructura': Tipo_Infraestructura,
'Tipo de Uso': Tipo_de_Uso,
'Tipo del Daño': Tipo_del_Danio,
'Verificado' : Verificado,
'Víveres Faltantes ': Viveres_Faltantes,
'Víveres Sobrantes ': Viveres_Sobrantes,
'latitud': latitud,
'longitud': longitud
	})

tedd.to_csv('/Users/parismendez/Desktop/TED_D.csv')