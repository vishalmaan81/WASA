const express = require('express');
const { spawn } = require('child_process');

const app = express();

app.get('/scan', (req, res) => {
  const url = req.query.url;

  const process = spawn('python', ['xss_scanner.py', url]);

  let output = '';
  process.stdout.on('data', data => {
    output += data;
  });

  process.stderr.on('data', data => {
    console.error(`Error: ${data}`);
  });

  process.on('close', code => {
    if (code !== 0) {
      console.error(`xss_scanner.py process exited with code ${code}`);
      res.status(500).send('Internal server error');
    } else {
      res.send(output);
    }
  });
});

const port = process.env.PORT || 5000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
