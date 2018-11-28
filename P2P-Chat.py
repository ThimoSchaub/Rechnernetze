import socket, pickle, struct
from _thread import start_new_thread
import threading
import _tkinter
from tkinter import *
from tkinter import scrolledtext


class message:
    msg = ""

    def __init__(self, msg):
        self.msg = msg


class join:
    name = ""

    def __init__(self, name):
        self.name = name


class exit:
    exit = "has left the chat"


buddylist = []
PORT = 50000
name = "Timo"
lock = threading.Lock()

def getSockofBuddy(s):
    for buddy in buddylist:
        if(buddy[0]== s):
            return buddy[2]
    return None

def getBuddyfromIp(s):
    for buddy in buddylist:
        if(buddy[1]== s):
            return True
    return False




def jointoserver(sock):
    try:
        packet = pickle.dumps(join(name))
        length = struct.pack('!I', len(packet))
        packet = length + packet
        sock.send(packet)
    except:
       print("IP " + sock + " refused the connection")


def sendmessagetoserver(sock,msg):
    packet = pickle.dumps(message(msg))
    length = struct.pack('!I', len(packet))
    packet = length + packet
    sock.send(packet)


def sendquittoserver(sock):
    packet = pickle.dumps(exit())
    length = struct.pack('!I', len(packet))
    packet = length + packet
    sock.send(packet)


def recjoin():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('141.37.168.38', PORT))
    s.listen(1)
    conn, addr = s.accept()
    buf = b''
    while len(buf) < 4:
        buf += conn.recv(4 - len(buf))
    length = struct.unpack('!I', buf)[0]
    msg = conn.recv(length)
    data_variable = pickle.loads(msg)
    if type(data_variable) is join:
        name = data_variable.name
        print("Recjoin gets name "+name)
        return name


def connect(s):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        ip = '141.37.168.' + str(s)
        print("Try to connect to ip:"+ip)
        sock.connect((ip, 50000))
        jointoserver(sock)
        # b_name = recjoin()
        # lock.acquire()
        # buddylist.append((b_name, ip, sock))
        # lock.release()
        #print('IP:' + ip + ' Nickname:' + b_name)
    except:
        print("Connection to " + ip + " failed")


#<editor-fold desc="Bedienelemente">
def scan(s):
    for i in range(s[0], s[1], 1):
        connect(i)


def list(l):
    for i in l:
        print("Nickname: "+i[0] + " is reachable under the IP: " + i[1])


def chat(c):
    msg = input("Enter  Message: ")
    sendmessagetoserver(c, msg)


def group_chat(g):
    for i in buddylist:
        sendmessagetoserver(i[2], g)


def quit(q):
    for i in q:
        sendquittoserver(i[2])
        i[2].close()
        buddylist.remove(i)
#</editor-fold>

def client():
    o = input("Type q for quit\n Type c for chat \n Type g for group chat \n Type l for list\n Type s for scan \n")
    if o == 'q':
        quit(buddylist)
    elif o == 'c':
        buddy = input("Type in the Name of the buddy to send a message only to him\n")
        sock = getSockofBuddy(buddy)
        if sock is None:
            print("Buddy isn't in the buddy list\n")
        else:
           chat(sock)
    elif o == 'l':
        list(buddylist)
    elif o == 's':
        scan([37, 40])
    elif o == 'g':
        msg = input("Enter Message")
        group_chat(msg)
    client()

def jointoserver(sock):
    try:
        packet = pickle.dumps(join(name))
        length = struct.pack('!I', len(packet))
        packet = length + packet
        sock.send(packet)
    except:
       print("IP " + sock + " refused the connection")


def recmessage(newsocket, addr):
    while True:
        buf = b''
        print(addr[0])
        while len(buf) < 4:
            buf += newsocket.recv(4 - len(buf))
        length = struct.unpack('!I', buf)[0]
        msg = newsocket.recv(length)
        data_variable = pickle.loads(msg)
        if type(data_variable) is join:
            name = data_variable.name
            print("Server gets name "+name)
            if not getBuddyfromIp(addr[0]):
                lock.acquire()
                buddylist.append((name, addr[0], newsocket))
                lock.release()
                #jointoserver(conn)
        elif type(data_variable) is message:
            msg = data_variable.msg
            print(name + ":" + msg)
        # elif(type(data_variable) is exit):

        else:
            print("unknown message typ")


def next_server(parentsocket):
    newsocket, addr = parentsocket.accept()
    print("Server started")
    start_new_thread(next_server, (parentsocket,))
    print('Connected by', addr)
    recmessage(newsocket, addr)



def server():
    HOST = '141.37.168.38'
    PORT = 50000
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen(12)
    start_new_thread(next_server,(serversocket,))

server()

client()

# start_new_thread(server,())
# gui()
# client()
# connect()


#
# s.send(message.encode('utf-8'))
# pickledResponse = s.recv(4096);
# response = pickle.loads(pickledResponse)
#
#
# response = pickle.loads(pickledResponse)
# EOFError: Ran out of input
