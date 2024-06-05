# HTTP Server - Express

Setting up a HTTP server and how to use common features in the express framework:

```javascript
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const server = require('http').Server(app);;

const PORT = 80;

/* Verify the JSON body has all of these properties.

   Input: POST Request Body and a List of Properties.
   Returns: TRUE is all properties are there, otherwise FALSE.
*/
const verifyPropertiesExists = (requestBody, propertyList) => {
	return propertyList.map(property => requestBody.hasOwnProperty(property)).every(result => result === true);
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

	

// Login API
app.post('/login', (req, res) => {
	console.log(req.body); // { username: 'John123', password: 'Password_ThatShouldNotBeGuessed641'}

	console.log(req.body.username); // 'John123'
	console.log(req.body.password); // 'Password_ThatShouldNotBeGuessed641'

	let loginSuccessful = false;

	if (req.body && req.body.username && req.body.password) {
		// Insert Authentication logic here
		loginSuccessful = true;
	}

	if (loginSuccessful) {
		// Login Successful, set a Cookie in the response
		res.cookie('auth-token', 'kln450x02sl5gusnh3mpu0s7ca2jfsaf8h', {
			maxAge: 3600000, 	// Time in milliseconds: 3600000 = 1 Hour
			httpOnly: true,
			sameSite: 'lax'
		}).send({ success: true });
	} else {
		// Login Failed
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