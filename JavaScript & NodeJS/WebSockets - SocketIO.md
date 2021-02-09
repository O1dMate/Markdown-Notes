# WebSockets - Socket IO

Example of how to setup a Socket IO server on top of a HTTPS Server using NodeJS and JavaScript:

<br>

## Install Requirements
```bash
npm i express socket.io
```

<br>

## Backend - NodeJS

```javascript
const express = require('express');
const path = require('path');
const fs = require('fs');
const ws = require('ws');
const app = express();

const HOSTNAME = 'host1.oldmate';
const PORT = 8443;

const serverOptions = {
	hostname: HOSTNAME,
	port: PORT,

	ca: fs.readFileSync(path.join(__dirname, 'certs/ca.crt')),
	cert: fs.readFileSync(path.join(__dirname, 'certs/host1.crt')),
	key: fs.readFileSync(path.join(__dirname, 'certs/host1.key')),
}

const httpServer = require('https').Server(serverOptions, app);
const io = require('socket.io')(httpServer);

// New WebSocket Connection
io.on('connection', (socket) => {
	let cookie = socket.handshake?.headers?.cookie || 'N/A';

	socket.on('/endpoint/1', (msg) => {
		console.log('/endpoint/1', msg);
	});

	socket.on('/endpoint/2', (msg) => {
		console.log('/endpoint/2', msg);
		socket.emit('/api/connected', 'Connection Success');
	});

	socket.on('/close-socket', () => {
		socket.disconnect();
	});

	socket.on('disconnect', () => {
		console.log('Socket Closed:', socket.id);
	});
});

httpServer.on('upgrade', (request, socket) => {
	console.log('here');
	socket.destroy();
});

app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, 'index.html'));
});


console.clear();

// Start the Server
httpServer.listen(PORT, () => {
	console.log(`[-] Server Listening on Port ${PORT}`);
});
```

<br>

## Frontend - HTML & JavaScript

```html
<!DOCTYPE html>
<html>
<head>
	<title>WebSocket - Socket IO</title>
</head>
<body>
	<h4>WebSocket - Socket IO</h4>

	<script src="/socket.io/socket.io.js"></script>
	<script>
		const socket = io('https://host1.oldmate:8443');

		socket.on('connect', () => {
			console.log('CONNECTED');
			socket.emit('/endpoint/2', 'Test Message');
		});

		socket.on('disconnect', () => {
			console.log('DISCONNECTED');
		});

		socket.on('/api/connected', (msg) => {
			console.log(`MSG:`, msg);
		});

		setTimeout(() => {
			socket.emit('/endpoint/2', 'Test Message');
		}, 1000)
	</script>
</body>
</html>
```