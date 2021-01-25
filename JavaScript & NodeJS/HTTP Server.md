# HTTP Server - Express

Setting up a HTTP server and how to use common features in the express framework:

```javascript
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const server = require('http').Server(app);;

const PORT = 80;

// Input: POST Request Body and a List of Properties. Verify the JSON body has all of these properties.
// Returns: TRUE is all properties are there, otherwise FALSE.
const verifyPropertiesExists = (requestBody, propertyList) => {
	return propertyList.map(property => requestBody.hasOwnProperty(property)).reduce((acum, cur) => acum && cur, true);
}

// Support JSON encoded POST request bodies
app.use(bodyParser.json());

// Handle decode error in-case an invalid URI is sent.
app.use((req, res, next) => {
	// Add custom Response Headers
	res.header('X-AspNet-Version', '4.0.30319');
	res.header('X-Powered-By', 'ASP.NET');

	try {
		decodeURIComponent(req.path)
		next();
	} catch (err) {
		res.sendStatus(404);
	}
});

// Redirect to another route
app.get('/', (req, res) => {
	res.redirect('home');
});

// Return HTML as a string. The type will automatically be set as HTML if a string is provided
app.get('/home', (req, res) => {
	res.send('<h1>Home</h1>');
});

// Return JSON. The type will automatically be set as JSON if an object is provided.
app.get('/json', (req, res) => {
	res.send({ json: true });
});

// Return anything you like, with a custom type.
app.get('/text', (req, res) => {
	res.type('txt');
	res.send('<h1>Home</h1>');
});

// Return a file from disk
app.get('/file', (req, res) => {
	res.sendFile(path.join(__dirname, 'index.html'));
});

// Request with Placeholder IDs and Query Parameters
app.get('/query/:idOne/:idTwo?/:idThree?', (req, res) => {
	// For the URI: /query/1/this/2?u=my%20data&help=true
	// req.params = { idOne: '1', idTwo: 'this', idThree: '2' }
	// req.query = { u: 'my data', help: 'true' }

	// Send custom HTTP Status code
	res.status(406).send('OK');
});

app.post('/login', (req, res) => {
	// Ensure we received the right params in the JSON body
	if (req.body && verifyPropertiesExists(req.body, ['username', 'password'])) {
		// If req.body is empty, ensure that "Content-Type: application/json" is set as a request header.
		
		// Get the params from the request body
		let username = (req.body.username || '').toString();
		let password = (req.body.password || '').toString();

		// Perform Authentication logic here

		// Login was successful, set a Cookie in the response
		res.cookie('MyCookie', 'abcdefghijklmnopqrstuvwxyz', {
			maxAge: 3600000, 	// Time in milliseconds: 3600000 = 1 Hour
			domain: 'localhost',
			path: '/',
			secure: true,
			httpOnly: true,
			sameSite: 'strict'
		}).send({ success: true });
	} else {
		res.send({ success: false });
	}
});

// Dealing with other HTTP Methods
app.get('/*', (_, res) => res.send({ success: false }));
app.post('/*', (_, res) => res.send({ success: false }));
app.put('/*', (_, res) => res.send({ success: false }));
app.delete('/*', (_, res) => res.send({ success: false }));
app.trace('/*', (_, res) => res.send({ success: false }));

// Catch any unforeseen errors
app.use((err, __, res, ___) => res.send({ success: false }));

// Start the Web-Server
server.listen(PORT, () => {
	console.log(`[+] Server Started Listening on Port ${PORT}`);
});
```