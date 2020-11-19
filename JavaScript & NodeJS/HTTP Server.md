# HTTP Server

```javascript
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const server = require('http').Server(app);;

const PORT = 80;

// Support JSON encoded POST request bodies
app.use(bodyParser.json());

// Handle decode error incase an invalid URI is sent.
app.use((req, res, next) => {
	try {
		decodeURIComponent(req.path)
		next();
	} catch (err) {
		res.sendStatus(404);
	}
})

app.get('/', (req, res) => {
	res.redirect('home');
});

app.get('/home', (req, res) => {
	res.send('<h1>Home</h1>');
});

app.get('/query/:idOne/:idTwo?/:idThree?', (req, res) => {
	// For the URI: /query/1/this/2?u=my%20data&help=true
	// req.params = { idOne: '1', idTwo: 'this', idThree: '2' }
	// req.query = { u: 'my data', help: 'true' }

	// Send custom HTTP Status code
	res.status(406).send('OK');
})

app.post('/login', (req, res) => {
	try {
		// Ensure we received the right params
		if (req.body && !req.body.hasOwnProperty('username') && req.body.hasOwnProperty('password')) {
			// Get the params from the request
			let username = (req.body.username || '').toString();
			let password = (req.body.password || '').toString();
		} else {
			res.send({ success: false });
		}
	} catch (err) {
		res.send({ success: false });
	}
});

server.listen(PORT, () => {
	console.log(`[-] Server Listening on Port ${PORT}`);
});
```