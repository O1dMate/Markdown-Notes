# Using Fetch

## GET Request
```javascript
fetch('/home');
```

<br>

## POST Request
```javascript
let apiData = { username:'username', password:'password' };

fetch('/login', { 
	method:'POST',
	headers: {
		'Content-Type': 'application/json'
	},
	body: JSON.stringify(apiData)
});
```

<br>

## Include Cookies for Cross-Domain Requests
```javascript
// The current origin is "https://my-domain.com".

// Cookies for "my-domain.com" will be sent in the request.
fetch('/home');

// Cookies for "testing.com" WILL NOT be sent in the request.
fetch('https://testing.com/home');

// Cookies for "testing.com" WILL be sent in the request.
fetch('https://testing.com/home', {
	credentials: 'include'
});
```

<br>

## Custom Headers
```javascript
fetch('/home', {
	headers: {
		'Custom-Header-1': 'My Custom Header 1',
		'Custom-Header-2': 'My Custom Header 2',
		'Authorization': ' Bearer myToken',
	},
});
```

<br>


## Response Data

Using Async & Await
```javascript
let responseData = await fetch('/api');
responseData = await responseData.json();

console.log(responseData); // { userId: 1, username: "admin" }
```

Using then/catch/finally
```javascript
fetch('/api').then(response => 
	response.json()	// .text() is valid if you want the data as a string instead
).then(data => {
	console.log(data); // { userId: 1, username: "admin" }
}).catch(err => {
	console.error(err);
});
```

<br>


## Response Headers/Status
```javascript
let response = await fetch('/api');

// Get the HTTP response code
console.log(response.status);

// Get a single header
console.log(response.headers.get('content-type'));

// Loop over all headers & values
response.headers.forEach((value, header) => {
	console.log(header, value);
});
```
