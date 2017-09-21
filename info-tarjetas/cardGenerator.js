const jsPDF = require('node-jspdf');

const saveCallback = err => {
  if (err)
    console.log(err);
  console.log('Generated');
};

const setColorBytype = (type) => {
  if (type === 'D')
    return [255, 72, 72];
  else
    return [0, 146, 69];
};

const createCard = (data) => {
  const c     = setColorBytype(data.type);
  const white = '#FFFFFF';
  const black = '#000000';
  const gap = 7.5;

  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'cm',
    format: [12, 10]
  });

  // Tipo
  doc.setFillColor(c[0], c[1], c[2]);
  doc.rect(0, 0, 1, 1, 'F');

  // Tipo texto
  doc.setTextColor(white);
  doc.setFontSize(16);
  doc.text(data.type, .3, .7);
  
  // Hashtag
  doc.setTextColor(black);
  doc.text('#Verificado19S', 1.1, .8);
  
  // Rectangulo fecha
  doc.setFillColor(c[0], c[1], c[2]);
  doc.rect(6.4, 0, 4, 1, 'F');

  // Fecha
  doc.setTextColor(white);
  doc.setFontSize(12);
  doc.text(data.date, 7, .7);

  // Riesgo
  doc.setFillColor(c[0], c[1], c[2]);
  doc.rect(1, 2, 7, 1, 'F');

  // Texto Riesgo
  doc.setTextColor(white);
  doc.setFontSize(16);
  doc.text(data.msg, 1.2, 2.7);

  // Direccion
  doc.setTextColor('#ff4848');
  doc.setFontSize(16);
  doc.setFontStyle('bold');
  doc.text(`${data.address.calle} ${data.address.nro}`, 1.5, 4.5);
  doc.text(data.address.col, 1.5, 5.5);

  // Falta
  doc.setTextColor(black);
  doc.setFontStyle('italic');
  doc.text('FALTA', 1.5, 7);
  doc.setFontStyle('normal');
  doc.setFontSize(10);
  data.falta.forEach((item, i) => doc.text(item, 1.5, gap + (i * 0.5)));

  // Sobra
  doc.setFontStyle('italic');
  doc.setFontSize(16);
  doc.text('SOBRA', 6, 7);
  doc.setFontStyle('normal');
  doc.setFontSize(10);
  data.sobra.forEach((item, i) => doc.text(item, 6, gap + (i * 0.5)));

  doc.save(`./pdf/${data.title}.pdf`, saveCallback);
};

// data.forEach(item => createCard(item));
module.exports.createCard = createCard;