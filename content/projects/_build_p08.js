const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, 'project-08.json');

const data = require('./_p08_parts.json');

fs.writeFileSync(OUT, JSON.stringify(data, null, 2), 'utf-8');
console.log('Written', fs.statSync(OUT).size, 'bytes');
