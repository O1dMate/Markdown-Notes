# Using Netcat

### Listen for Connections
```bash
nc -lvp PORT_NUMBER
```
- TCP is default. Add a `-u` flag for UDP connections.
- `l` is for listen mode, the computer will wait for a connection rather then making one.
- `v` if for verbose mode.
- `p` is to specify a port number.
- You can test this is working by going to your web browser and entering this in the URL bar: `COMPUTER_IP:PORT_NUMBER`



### Send File From Host to Host
- File transfer using netcat are `NOT` encrypted, use only on trusted networks.

#### Sender
```bash
nc -v -w 3 COMPUTER_IP PORT_NUMBER < INPUT_FILE
```
 - `-w 3` means wait set the connection timeout to 3 seconds.

#### Receiver
```bash
nc -lvp PORT_NUMBER > OUTPUT_FILE
```


### Test for Plaintext SMTP Login
```bash
nc -nv SERVER_IP PORT_NUMBER
EHLO HOSTNAME
```
- `-n` is for no DNS resolution.
- `EHLO` is if the server is ESMTP. Standard SMTP should use `HELO` prefix. 
