# -*- coding: utf-8 -*-

# Diccionarios feos para realizar migración de tablas


# Para homogeneizar spreadsheets O/D con Big Query:
gsheets_bquery = {'Alimentos Existentes (por favor, separa tu respuesta por comas)': 'AlimentosExistentes',
    'Alimentos Faltantes (por favor, separa tu respuesta por comas)': 'AlimentosFaltantes',
    'Artículos Urgentes (por favor, separa tu respuesta por comas)': 'ArtculosUrgentes',
    'Calle': 'Calle',
    'Colonia': 'Colonia',
    'Delegación o municipio': 'Delegacinomunicipio',
    'En operación': 'operando',
    'Estado': 'Estado',
    'Herramientas Existentes (por favor, separa tu respuesta por comas)': 'HerramientasExistentes',
    'Herramientas Faltantes (por favor, separa tu respuesta por comas)': 'HerramientasFaltantes',
    'Horario de atención': 'Horariodeatencin',
    'Timestamp': 'Marcatemporal',
    'Medicamentos Existentes(por favor, separa tu respuesta por comas)': 'MedicamentosExistentes',
    'Medicamentos Faltantes (por favor, separa tu respuesta por comas)': 'MedicamentosFaltantes',
    'Nombre del centro': 'Nombredelcentro',
    'Nombre del contacto (esta información no se ha pública)': 'Nombredelcontacto',
    'Número (aproximado al menos)': 'Nmero',
    'Otros Artículos que Necesitan (por favor, separa tu respuesta por comas)': 'OtrosArtculosqueNecesitan',
    'Se requiere voluntarios': 'Serequierevoluntarios',
    'Teléfono (esta información no se hará pública)': 'Telfono',
    'Verificado': 'Verificado'
    }


# Para crear nombres de columnas más utilizables:
bquery_clean = {'int64_field_0': 'id_pet',
    'AlimentosExistentes': 'alimentos',
    'AlimentosFaltantes': 'alimentos_f',
    'ArtculosUrgentes': 'articulos_f',
    'Calle': 'dir_calle',
    'Colonia': 'dir_col',
    'Delegacinomunicipio': 'dir_del',
    'EspecialistasExistentesseparaporcomas': 'especialistas',
    'EspecialistasFaltantesseparaporcomas': 'especialistas_f',
    'Estado': 'dir_estado',
    'HerramientasExistentes': 'herramientas',
    'HerramientasFaltantes': 'herramientas_f',
    'Horariodeatencin': 'horario',
    'Marcatemporal': 'timestamp',
    'MedicamentosExistentes': 'medicamentos',
    'MedicamentosFaltantes': 'medicamentos_f',
    'Nombredelcentro': 'centro_nom',
    'Nombredelcontacto': 'contacto_nom',
    'Nmero': 'dir_num',
    'OtrosArtculosqueNecesitan': 'articulos',
    'Serequierevoluntarios': 'voluntarios',
    'Telfono': 'dir_tel',
    'TelfonoAcopio': 'centro_tel',
    'Verificado': 'verificado',
    'latitud': 'lat',
    'longitud': 'lng'
    }


# Índice de las columnas a checar para aplicar clean_list
check_list = ['alimentos', 
             'alimentos_f', 
             'articulos',
             'especialistas',
             'especialistas_f',
             'herramientas',
             'herramientas_f',
             'medicamentos',
             'medicamentos_f',
             'voluntarios'
             ]


# Traduce valores. Ahorita sólo tiene a None. Fase 2: corregir typos?
clean_list = {' ': None,
              '0': None, 
              '.': None,
              '-': None,
              'atendido': None,
              'cero': None,
              'de todos': None,
              'de todas': None,
              'de todo un poco': None,
              'desabasto': None,
              'esenciales': None,
              'na': None,
              'n/a': None,
              'nan': None, 
              'nada': None,
              'ninguno': None,
              'no': None,
              'no aplica': None,
              'no aplica por el momento': None,
              'no ahorita': None,
              'no hay informacion': None,
              'no hay respuesta': None,
              'no estan recibido': None,
              'no estan recibiendo': None,
              'no estan solicitando donaciones': None,
              'no se': None,
              'no se necesitan': None,
              'no tenemos viveres': None,
              'recopilando informacion': None,
              'sin respuesta': None,
              'todos': None,
              'tienen': None,
              'varios': None,
              'x': None,
              }

