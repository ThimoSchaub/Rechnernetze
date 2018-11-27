import socket, pickle, struct
from _thread import start_new_thread
import threading
import _tkinter
from tkinter import *
from tkinter import scrolledtext


class message:
    msg = ""
    def __init__(self,msg):
        self.msg = msg

class join:
    name = ""
    def __init__(self,name):
        self.name = name

class exit:
    exit = "has left the chat"

buddylist=[]
PORT= 50000
name = "T(h)imo"

def client():
    jointoserver('localhost')
    exit = False
    while not exit:
        msg = input("Insert Message: ")
        sendmessagetoserver('localhost',msg)
    s.close()
    print('Data Sent to Server')

def jointoserver(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip,PORT))
    packet = pickle.dumps(join(name))
    length = struct.pack('!I', len(packet))
    packet = length + packet
    s.send(packet)

def sendmessagetoserver(ip,msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, PORT))
    packet = pickle.dumps(message(msg))
    length = struct.pack('!I', len(packet))
    packet = length + packet
    s.send(packet)

def server():
    HOST = '141.37.168.38'
    PORT = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(12)
    conn, addr = s.accept()
    print('Connected by', addr)

    while True:
        buf = b''
        while len(buf) < 4:
            buf += conn.recv(4 - len(buf))
        length = struct.unpack('!I', buf)[0]
        msg = conn.recv(length)
        data_variable = pickle.loads(msg)
        if type(data_variable) is join:
            name = data_variable.name
        elif type(data_variable) is message:
            msg = data_variable.msg
            print(name+":" + msg)
        # elif(type(data_variable) is exit):

        else:
            print("unknown message typ")
    conn.close()
    print(data_variable)
    # Access the information by doing data_variable.process_id or data_variable.task_id etc..,
    print('Data received from client')


def clicked():
    client()


def recjoin():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('141.37.168.38', PORT))
    s.listen(12)
    conn, addr = s.accept()
    buf = b''
    while len(buf) < 4:
        buf += conn.recv(4 - len(buf))
    length = struct.unpack('!I', buf)[0]
    msg = conn.recv(length)
    data_variable = pickle.loads(msg)
    if type(data_variable) is join:
        name = data_variable.name
        return name

def connect():
    for i in range(30, 42, 1):
        t = threading.Thread(target=scan,args=[i])
        t.start()

def scan(s):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ip = '141.37.168.' + str(s)
        sock.connect((ip, 50000))
        jointoserver(ip)
        name = recjoin()
        print('IP:'+ip+' Nickname:'+name)
    except :
        print("Ip "+ip+ " does not respond")
        pass
        # print("Fehler "+str(i)+"\r\n")


# def list(l):
#
# def chat(c):
#
# def group_chat(g):
#
# def quit(Q):


#server()
#start_new_thread(server,())
#gui()
#client()
connect()




#
# s.send(message.encode('utf-8'))
# pickledResponse = s.recv(4096);
# response = pickle.loads(pickledResponse)
#
#
# response = pickle.loads(pickledResponse)
# EOFError: Ran out of input
