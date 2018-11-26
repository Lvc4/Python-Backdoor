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
    pfilename = bef[1]
    print("put " + str(pfilename) + " >>")
    pfile = open(pfilename, "rb")
    pdata = pfile.read()
    psize = os.path.getsize(pfilename)
    connection.send(bytes(str(pfilename), "utf8"))
    connection.send(bytes(str(psize), "utf8"))
    connection.send(pdata)
   
def get(befehl):
    bef = befehl.split(" ")
    gfilename = bef[1]
    print("get " + str(gfilename) + " >>")
    connection.send(bytes(str(gfilename), "utf8"))
    gsi = connection.recv(256)
    gsize = int(str(gsi, "utf8"))
    gdata = connection.recv(gsize)
    gfile = open(str(gfilename), "wb")
    gfile.write(gdata)
    gfile.flush()
    gfile.close()

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
            outp = str(output, "utf8")
            print (outp)

command()