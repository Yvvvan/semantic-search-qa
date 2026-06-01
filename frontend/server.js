const http = require('http');
const fs = require('fs');
const path = require('path');

const port = Number(process.env.PORT || 4200);
const root = path.join(__dirname, 'dist', 'SearchQAArbeitsrecht');

const contentTypes = {
  '.css': 'text/css',
  '.html': 'text/html',
  '.ico': 'image/x-icon',
  '.jpg': 'image/jpeg',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.map': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain',
};

function sendFile(response, filePath) {
  const extension = path.extname(filePath).toLowerCase();
  const contentType = contentTypes[extension] || 'application/octet-stream';

  fs.readFile(filePath, (error, content) => {
    if (error) {
      response.writeHead(500, { 'Content-Type': 'text/plain' });
      response.end('Internal Server Error');
      return;
    }

    response.writeHead(200, { 'Content-Type': contentType });
    response.end(content);
  });
}

http
  .createServer((request, response) => {
    const requestPath = decodeURIComponent(request.url.split('?')[0]);
    const normalizedPath = path.normalize(requestPath).replace(/^(\.\.[/\\])+/, '');
    const filePath = path.join(root, normalizedPath === '/' ? 'index.html' : normalizedPath);

    if (!filePath.startsWith(root)) {
      response.writeHead(403, { 'Content-Type': 'text/plain' });
      response.end('Forbidden');
      return;
    }

    fs.stat(filePath, (error, stats) => {
      if (!error && stats.isFile()) {
        sendFile(response, filePath);
        return;
      }

      sendFile(response, path.join(root, 'index.html'));
    });
  })
  .listen(port, '0.0.0.0', () => {
    console.log(`Frontend listening on ${port}`);
  });
