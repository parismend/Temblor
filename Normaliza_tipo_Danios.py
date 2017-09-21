import pandas as pd
from Dicc_Tipo_Danhos import camb_tipos

def camb_tipos():
	uni_Tipos = ['Fuga de Gas',
	'Daños estructural verificado por proteccion civil',
	'Derrumbe, Desalojado/Acordonado, Fuga de Gas',
	'Derrumbe, Desalojado/Acordonado',
	'Desalojado/Acordonado',
	'Explosion de pipa',
	'Daño estructural',
	'Fractura de muro en colindancia',
	'Edificio agrietado ',
	'Grietas por cortante',
	'Cuarteadura y daño',
	'Grietas diagonales',
	'Hoyos en paredes y techo. Grietas',
	'Derrumbe',
	'Escaleras desniveladas',
	'Fuga de Agua',
	'fracturas inportantes ',
	'Desalojado/Acordonado, Está cerrado. No da servicio.',
	'Por colapsar posiblemente',
	'Agrietamiento',
	'Daño',
	'Riesgo de derrumbe',
	'Desalojado/Acordonado, Algunas columnas rodas dobladas ligeramente',
	'Edificios ladeados',
	'Derrumbe de barda',
	'Grietas en planta baja',
	'Fisuras estructurales y daños en losas',
	'Daños estructurales',
	'Derrumbe, Fuga de Gas',
	'dañado' ]	

	Tipos_unif = [
	'Fuga de Gas',
	'Daño Mayor',
	'Derrumbe',
	'Derrumbe',
	'Daño',
	'Daño',
	'Daño',
	'Daño',
	'Daño',
	'Daño',
	'Daño',
	'Daño',
	'Daño',
	'Derrumbe',
	'Daño',
	'Daño',
	'Daño',
	'Daño',
	'Daño Mayor',
	'Daño',
	'Daño',
	'Daño Mayor',
	'Daño',
	'Daño Mayor',
	'Derrumbe',
	'Daño',
	'Daño Mayor',
	'Daño Mayor',
	'Derrumbe',
	'Daño'
	]

	danhos_tipos = zip(uni_Tipos,Tipos_unif)
	Danho  = dict(danhos_tipos)

	return Danho

dicc_dho = camb_tipos()
info_pub.replace({'Tipo de Daños' : dicc_dho})



