from socket import *
import os

HOST = ''
PORT = 9999

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

print (">> Warten auf Verbindung an PORT " + str(PORT))

connection, adresse = s.accept()
print (">> Verbunden mit => " + str(adresse[0]))

def put(befehl):
    bef = befehl.split(" ")
    filename = bef[1]
    file = open(filename, "rb")
    data = file.read()
    size = os.path.getsize(filename)
    print(filename , size)
    connection.send(bytes(str(filename), "utf8"))
    connection.send(bytes(size, "utf8"))
    connection.send(data)
    


def command():
    while True:
        befehl = input(str(adresse[0]) + " >> ")
        connection.send(bytes(befehl, "utf8"))
        if befehl == "quit" :
            connection.close()
            break
        elif "put" in befehl: put(befehl)
        elif "get" in befehl: get(befehl)
        else:
            output = connection.recv(1024)
            print (str(output, "utf8"))

command()
