const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs').promises;

const app = express();
const label = {};

app.use(express.static(__dirname));
app.use(bodyParser.text({ type: 'text/html', limit: '50mb' }));

app.post('/save', async (req, res) => {
  res.send();
  let { body } = req;
  let [fileName, data] = body.split(',');
  fs.writeFile(__dirname + '/imgs/' + fileName, Buffer.from(data, 'base64'));
});

app.listen(8080, () => {
  console.log('Server opened.');
});