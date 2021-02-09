# WebSockets - Native

Example of how to setup a WebSocket server on top of a HTTPS Server using NodeJS and JavaScript:

<br>

## Install Requirements
```bash
npm i express ws
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
const webSocketServer = new ws.Server({ noServer: true });

// Handle WebSocket Connections (After Upgrade)
webSocketServer.on('connection', (socket, req) => {
	console.log('New WebSocket connection', req.socket.remoteAddress);

	socket.on('message', (msg) => {
		console.log('New MSG:', msg);
		socket.send('Received');
	});

	socket.on('error', (err) => {
		console.log('ERROR:', err);
		socket.terminate();
	});
});

// Handle WebSocket Upgrade
httpServer.on('upgrade', (request, socket, head) => {
	// Connection IP
	console.log(socket.remoteAddress);

	// Check the Origin is correct
	if (request.headers.origin === `https://${HOSTNAME}:${PORT}`) {

		// Check Cookie is valid here
		console.log(request.headers.cookie);

		// Upgrade the connection to a WebSocket
		webSocketServer.handleUpgrade(request, socket, head, (newSocket) => {
			webSocketServer.emit('connection', newSocket, request)
		});
	} else {
		socket.write('HTTP/1.1 401 Unauthorized\r\nConnection: close\r\n\r\n');
		socket.destroy();
	}
})


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
	<title>WebSockets - Native</title>
</head>
<body>
	<h4>WebSockets - Native</h4>

	<script>
		connectSocket = (url, params) => {
			let socket = new WebSocket(url, params);

			socket.onopen = () => {
				console.log("OPENED");
				socket.send('Test Message');
			}

			socket.onmessage = (msg) => {
				console.log(`MSG: "${msg.data}"`);
			}

			socket.onerror = (err) => {
				console.log("ERROR", err);
			}

			socket.onclose = () => {
				console.log("CLOSED");
			}

			return socket;
		}

		let socket = connectSocket('wss://host1.oldmate:8443');
	</script>
</body>
</html>
```