# -*- coding: utf-8 -*-

# Diccionarios feos para realizar migración de tablas

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

bquery_clean = {'int64_field_0': 'id_pet',
    'AlimentosExistentes': 'alimentos',
    'AlimentosFaltantes': 'alimentos_f',
    'ArtculosUrgentes': 'articulos_f',
    'Calle': 'dir_calle',
    'Colonia': 'dir_col',
    'Delegacinomunicipio': 'dir_del',
    'EspecialistasExistentesseparaporcomas': 'especialistas',
    'EspecialistasFaltantesseparaporcomas': 'especialistas_f',
    'Estado': 'estado',
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
    'latitud': 'lat_long'
}

