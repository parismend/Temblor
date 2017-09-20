const jsPDF = require('node-jspdf');

const doc = new jsPDF({
  orientation: "portrait",
  unit: "cm",
  format: [12, 10]
});

const saveCallback = err => {
  if (err)
    console.log(err);
  console.log("Generated");
};

const createCard = () => {
  // Tipo
  doc.setFillColor(255, 72, 72);
  doc.rect(0, 0, 1, 1, 'F');

  // Tipo texto
  doc.setTextColor("#FFFFFF");
  doc.setFontSize(16);
  doc.text("R", .3, .7);
  
  // Hashtag
  doc.setTextColor("#000000");
  doc.text("#Verificado19S", 1.1, .8);
  
  // Rectangulo fecha
  doc.setFillColor(255, 72, 72);
  doc.rect(6.4, 0, 4, 1, 'F');

  // Fecha
  doc.setTextColor("#FFFFFF");
  doc.setFontSize(12);
  doc.text('20/9/17 12:26', 7, .7);

  // Riesgo
  doc.setFillColor(255, 72, 72);
  doc.rect(1, 2, 7, 1, 'F');

  // Texto Riesgo
  doc.setTextColor("#FFFFFF");
  doc.setFontSize(16);
  doc.text('FUGA DE GAS', 1.2, 2.7);

  // Direccion
  doc.setTextColor("#ff4848");
  doc.setFontSize(16);
  doc.setFontStyle("bold");
  doc.text("Calle Augusto Rodin 241", 1.5, 4.5);
  doc.text("Col. Noche Buena", 1.5, 5.5);

  // Falta
  doc.setTextColor("#000000");
  doc.setFontStyle("italic");
  doc.text("FALTA", 1.5, 7);
  doc.setFontStyle("normal");
  doc.setFontSize(10);
  doc.text("Ropa", 1.5, 7.5);
  doc.text("Viveres", 1.5, 8);
  doc.text("Medicinas", 1.5, 8.5);
  doc.text("Alimientos preparados", 1.5, 9);

  // Sobra
  doc.setFontStyle("italic");
  doc.setFontSize(16);
  doc.text("SOBRA", 6, 7);
  doc.setFontStyle("normal");
  doc.setFontSize(10);
  doc.text("Ropa", 6, 7.5);
  doc.text("Viveres", 6, 8);
  doc.text("Medicinas", 6, 8.5);
  doc.text("Alimientos preparados", 6, 9);

  doc.save('./pdf/card3.pdf', saveCallback);
};

createCard();