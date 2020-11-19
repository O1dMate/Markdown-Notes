# Certificate Based Mutual Authentication

Example of how to setup Cert-Based Mutual Auth for a NodeJS web server:


```javascript
const express = require('express');
const path = require('path');
const fs = require('fs');
const tls = require('tls');
const app = express();

const HOSTNAME = 'host1.oldmate';
const PORT = 4443;

const serverOptions = {
	hostname: HOSTNAME,
	port: PORT,

	// Certificates
	ca: fs.readFileSync(path.join(__dirname, 'certs/ca.crt')),
	cert: fs.readFileSync(path.join(__dirname, 'certs/host1.crt')),
	key: fs.readFileSync(path.join(__dirname, 'certs/host1.key')),

	// Cert-Based Mutual Auth settings
	requestCert: true,
	rejectUnauthorized: true,

	// TLS Settings
	minVersion: 'TLSv1.3',
	maxVersion: 'TLSv1.3',

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
})

// Handle Cert-Based Mutual Auth
// This isn't really required if `rejectUnauthorized` is `true`.
app.use((req, res, next) => {
	try {
		const cert = req.socket.getPeerCertificate();

		if (req.client.authorized) {
			next();
			// res.send(`Your certificate ${cert.subject.CN} was issued by ${cert.issuer.CN}`);
		} else if (cert.subject) {
			res.status(403).send(`Not Authorised`);
			// res.send(`Certificates from ${cert.issuer.CN} are not valid. User ${cert.subject.CN},`);

		} else {
			res.status(403).send(`Not Authorised`);
			// res.send(`Certificate Required`);
		}
	} catch (err) {
		res.sendStatus(404);
	}
})

app.get('/', (req, res) => {
	const cert = req.socket.getPeerCertificate() || { subject: {} };

	console.log(`Home Page Requested by: "${cert.subject.CN}"`);

	res.header('Content-Security-Policy',`default-src 'self' https://${HOSTNAME}:${PORT}`);
});

console.clear();

// Start the Server
server.listen(PORT, () => {
    console.log(`[-] Server Listening on Port ${PORT}`);
});
```