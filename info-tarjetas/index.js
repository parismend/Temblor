const mock = require('./dataParser').mockData;
const genCard = require('./cards').createCard;
const csvUrl = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRvxlMpfCKHJ11vHpLkrkUszgLTYAQ0bAd3a_RSGX6Gr06cKWh8IOqBDrd9A9qiN8Y5wv9e1d01mK2d/pub?gid=352754790&single=true&output=csv';

mock('D', csvUrl)
  .then(data => data.forEach(item => genCard(item)));
