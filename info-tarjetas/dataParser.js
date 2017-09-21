const d3 = require('d3');
const csvUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRvxlMpfCKHJ11vHpLkrkUszgLTYAQ0bAd3a_RSGX6Gr06cKWh8IOqBDrd9A9qiN8Y5wv9e1d01mK2d/pub?gid=352754790&single=true&output=csv';

const validateField = (fieldData, field, item) => {
  const standarStr = 'Si tienes info entra a: http://bit.ly/Verificado19s';
  const caseOne    = 'No hay actividad cerca del edificio. NO está derrumbado. Pasé esta mañana. Tengo fotos.';

  switch (fieldData) {
    case undefined:
      return [];
    case '':
      return [];
    case 'nose':
      return [];
    case 'No se':
      return [];
    case 'Ninguna':
      return [];
    case 'Ninguno':
      return [];
    case 'Nada':
      return [];
    case 'Nada.':
      return [];
    case standarStr:
      return [];
    case caseOne:
      return [];
    default:
      return item[field].split(',');
  }
};

module.exports.data = d3.csv(csvUrl, (err, data) => {
  if (err) console.log(err);

  data = data.filter(item => item['Verificado'] === 'Sí');

  const newData = data.map(item => {
    const mock = {};
    mock.dir   = { col: item['Colonia'], calle: item['Calle'], nro: item['Número Exterior  o Aproximado'] };
    mock.tipo  = 'D';
    mock.fecha = item['Timestamp'];
    mock.msj   = item['Tipo del Daño'];

    const herramientasFaltantes = validateField(
      item['Herramientas Faltantes'],
      'Herramientas Faltantes',
      item
    );

    const viveresFaltantes = validateField(
      item['Víveres Faltantes (por favor, separa tu respuesta por comas)'],
      'Víveres Faltantes (por favor, separa tu respuesta por comas)',
      item
    );

    const viveresSobrantes = validateField(
      item['Víveres Sobrantes'],
      'Víveres Sobrantes',
      item
    );

    const herramientasSobrantes = validateField(
      item['Herramientas Sobrantes'],
      'Herramientas Sobrantes',
      item
    );

    mock.falta = [...herramientasFaltantes, ...viveresFaltantes];
    mock.sobra = [...viveresSobrantes, ...herramientasSobrantes];
    return mock;
  });

  return newData;
});
