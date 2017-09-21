import pandas as pd

waze = pd.read_csv('datos/Mexico Earthquake Waze Pins.csv')

Calle=[''  for x in range(0,136)]
Colonia=[''  for x in range(0,136)]
Delegación=[''  for x in range(0,136)]
Foto=[''  for x in range(0,136)]
Herramientas_Faltantes =[''  for x in range(0,136)]
Herramientas_Sobrantes =[''  for x in range(0,136)]
Hora=[''  for x in range(0,136)]
Hora_Reporte=[''  for x in range(0,136)]
Mano_Faltante =[''  for x in range(0,136)]
Mano_Sobrantes =[''  for x in range(0,136)]
Mano_Sobrantes_Row_2=[''  for x in range(0,136)]
Mano_Sobrantes_Row_3=[''  for x in range(0,136)]
Mano_Sobrantes_Row_4=[''  for x in range(0,136)]
Medicamentos_Faltantes =[''  for x in range(0,136)]
Medicamentos_Sobrantes =[''  for x in range(0,136)]
Numero_Exterior_Aproximado =[''  for x in range(0,136)]
Numero_de_Personas_Atrapadas=[''  for x in range(0,136)]
Numero_de_Personas_Desaparecidas=[''  for x in range(0,136)]
Numero_de_Personas_Fallecidas=[''  for x in range(0,136)]
Numero_de_Personas_Lesionadas=[''  for x in range(0,136)]
Numero_de_Personas_Rescatadas=[''  for x in range(0,136)]
Otra_Referencia_de_Ubicación =[''  for x in range(0,136)]
Tipo_de_Infraestructura=[''  for x in range(0,136)]
Tipo_de_Uso=[''  for x in range(0,136)]
Tipo_del_Danho=[''  for x in range(0,136)]
Viveres_Faltantes =[''  for x in range(0,136)]
Viveres_Sobrantes =[''  for x in range(0,136)]
latitud=[''  for x in range(0,136)]
longitud=[''  for x in range(0,136)]

Calle = waze['address']
Colonia =  waze['additional_info']
Tipo_del_Danho = waze['pin_name']
for x in range(0,len(Tipo_del_Danho)):
	if (Tipo_del_Danho[x] == 'Zona de derrumbre'):
		Tipo_del_Danho[x] = 'Derrumbe'
latitud = waze['lat']
longitud = waze['lon']


waze_n = pd.DataFrame({
'Calle': Calle,
'Colonia': Colonia,
'Delegación': Delegación,
'Foto': Foto,
'Herramientas Faltantes': Herramientas_Faltantes,
'Herramientas Sobrantes': Herramientas_Sobrantes,
'Hora': Hora,
'Hora del Reporte': Hora_Reporte,
'Mano de Obra Faltante': Mano_Faltante,
'Mano de Obra Sobrantes': Mano_Sobrantes,
'Mano de Obra Sobrantes  [Row 2]': Mano_Sobrantes_Row_2,
'Mano de Obra Sobrantes  [Row 3]': Mano_Sobrantes_Row_3,
'Mano de Obra Sobrantes  [Row 4]': Mano_Sobrantes_Row_4,
'Medicamentos Faltantes': Medicamentos_Faltantes,
'Medicamentos Sobrantes': Medicamentos_Sobrantes,
'Número Exterior  o Aproximado': Numero_Exterior_Aproximado,
'Número de Personas Atrapadas': Numero_de_Personas_Atrapadas,
'Número de Personas Desaparecidas': Numero_de_Personas_Desaparecidas,
'Número de Personas Fallecidas': Numero_de_Personas_Fallecidas,
'Número de Personas Lesionadas': Numero_de_Personas_Lesionadas,
'Número de Personas Rescatadas': Numero_de_Personas_Rescatadas,
'Otra Referencia de Ubicación ': Otra_Referencia_de_Ubicación,
'Tipo de Infraestructura': Tipo_de_Infraestructura,
'Tipo de Uso': Tipo_de_Uso,
'Tipo del Daño': Tipo_del_Danho,
'Víveres Faltantes ': Viveres_Faltantes,
'Víveres Sobrantes ': Viveres_Sobrantes,
'latitud': latitud,
'longitud': longitud
	})



waze_n.to_csv('datos/waze.csv')

























