# SNI - Server Name Indication

Example of how to setup SNI for a NodeJS web server using the express framework.

```javascript
const express = require('express');
const path = require('path');
const fs = require('fs');
const tls = require('tls');
const app = express();

const PORT = 4443;
const sniDefaultCert = fs.readFileSync(path.join(__dirname, 'certs/host1.crt'));
const sniDefaultKey = fs.readFileSync(path.join(__dirname, 'certs/host1.key'));

const sniCallback = (serverName, callback) => {
	let cert = null;
	let key = null;

	if (serverName === 'host2.oldmate') {
		cert = fs.readFileSync(path.join(__dirname, 'certs/host2.crt'));
		key = fs.readFileSync(path.join(__dirname, 'certs/host2.key'));
	} else {
		cert = sniDefaultCert;
		key = sniDefaultKey;
	}

	callback(null, new tls.createSecureContext({
		cert,
		key,
	}));
}

const serverOptions = {
	port: PORT,

	SNICallback: sniCallback,

	// CA Certificate
	ca: fs.readFileSync(path.join(__dirname, 'certs/ca.crt')),

	// TLS Settings
	minVersion: 'TLSv1.3',
	maxVersion: 'TLSv1.3',

	// Optional: For hardened configuration
	echdCurve: 'secp384r1',
	ciphers: 'TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256',
	sigalgs: 'ecdsa_secp384r1_sha384',

	// Attempt to user Server cipher suite preference instead of clients.
	honorCipherOrder: true
}

const server = require('https').Server(serverOptions, app);

// Handle decode error incase an invalid URI is sent.
app.use((req, res, next) => {
	try {
		decodeURIComponent(req.path)
		next();
	} catch (err) {
		res.sendStatus(404);
	}
});

app.get('/', (req, res) => {
	// DO NOT use `req.hostname`, this gets the value from the `Host` header provided by the client.
	console.log(req.socket.servername);

	res.send(`<h1>Welcome</h1>`);
});

// Catch any unforeseen errors
app.use((err, __, res, ___) => res.send({ success: false }));

// Start the Server
server.listen(PORT, () => {
    console.log(`[-] Server Listening on Port ${PORT}`);
});
```