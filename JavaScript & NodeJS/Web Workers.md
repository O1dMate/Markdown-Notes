# Web Workers

Boilerplate code for setting up and using Web Workers in the Browser:

### HTML Code
```html
<!DOCTYPE html>
<html>
<head>
	<title>Web Workers</title>

	<!-- General Styling -->
	<style type="text/css">
		body {
			background-color: #444;
		}
		h3 {
			color: #ddd;
		}

	</style>
</head>
<body>
	<h3>Web Workers</h3>

	<script type="text/javascript">
		console.log('Creating Web Worker(s)...');

		const workerOnMessageHandler = ({ data }) => {
			let { workerId, action, outputData} = data;

			if (action === 'console.log') {
				console.log(...outputData);
			} else if (action = 'randomNumber') {
				console.log(`Random Number Results from Worker ${workerId}:`, outputData);
			}

		}

		const totalWorkers = 4;

		let workerList = [];

		// Create a list of Worker Objects
		for (let i = 0; i < totalWorkers; ++i) {
			let workerObj = new Worker('my-worker.js');

			workerObj.onmessage = workerOnMessageHandler;

			workerList.push({ workerId: i, workerObj })
		}

		// Send a task to each worker
		workerList.forEach(currentWorker => {
			currentWorker.workerObj.postMessage({
				workerId: currentWorker.workerId,
				action: 'randomNumber',
				inputData: 1000
			});
		});
	</script>
</body>
</html>
```


### Worker Code
```javascript
const printMessage = (workerId, ...msg) => {
	self.postMessage({
		workerId,
		action: 'console.log',
		outputData: msg
	});
}

const calculations = (inputData) => {
	return Math.round(Math.random()*inputData);
}

self.onmessage = ({ data }) => {
	let { workerId, action, inputData } = data;

	printMessage(workerId, `Worker (${workerId}) Received Message "${action}":`, inputData);

	if (action === 'randomNumber') {
		let result = calculations(inputData);

		self.postMessage({ workerId, action, outputData: result });
	}
}
```
