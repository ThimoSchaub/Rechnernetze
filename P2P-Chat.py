import struct
from socket import *
from _thread import start_new_thread
import pickle
import sys
import time


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


class Buddy:
    def __init__(self, name, conn, addr):
        self.name = name
        self.conn = conn
        self.addr = addr

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.name == other.name and self.addr == other.addr


USERNAME = "DieTimos"
HOST = gethostbyname(gethostname())
IPS = ["141.37.168.40", "141.37.168.41"]
#HOST = "127.0.0.4"
PORT = 50000
BUDDYS = []
THREAD_RUNNING = True
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(10)


def exec_join(name, conn, addr):
    tmp = Buddy(name, conn, addr)
    if tmp not in BUDDYS:
        BUDDYS.append(tmp)
        packet = pickle.dumps(join(USERNAME))
        length = struct.pack('!I', len(packet))
        packet = length + packet
        conn.send(packet)
        print(str(tmp.name) + " connected.\n")


def exec_message(msg, conn):
    name = "n.a."
    for b in BUDDYS:
        if b.conn == conn:
            name = b.name
    print(str(name) + ": " + str(msg))


def exec_exit(conn):
    i = 0
    for b in BUDDYS:
        if b.conn == conn:
            b.conn.close()
            del BUDDYS[i]
            break
        i += 1


def listen_all():
    while THREAD_RUNNING:
        (conn, addr) = sock.accept()
        start_new_thread(handle_connection, (conn, addr))
    sock.close()


def handle_connection(conn, addr):
    while THREAD_RUNNING:
        buf = b''
        while len(buf) < 4:
            try:
                time.sleep(1)
                buf += conn.recv(4 - len(buf))
            except WindowsError:
                pass
        print("recv Message")
        length = struct.unpack('!I', buf)[0]

        text = conn.recv(length)

        text = pickle.loads(text)
        if type(text) is join:
            exec_join(text.name, conn, addr)
        elif type(text) is exit:
            exec_exit(conn)
        elif type(text) is message:
            exec_message(text.msg, conn)
        else:
            print("recv message is not valid\n")



def scan_open():
    try:
        for ip in IPS:
            scan_sock = socket(AF_INET, SOCK_STREAM)
            result = scan_sock.connect_ex((ip, PORT))
            if result == 0:
                print("connect to ip: " + str(ip))
                send_join(join(USERNAME), (ip, PORT))
            scan_sock.close()

    except gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    except error:
        print("Couldn't connect to server")
        sys.exit()


def send_join(packet, addr):
    sock_remote = socket(AF_INET, SOCK_STREAM)
    packet = pickle.dumps(packet)
    length = struct.pack('!I', len(packet))
    packet = length + packet
    sock_remote.connect(addr)
    tmp = Buddy(USERNAME, sock_remote, addr)
    if tmp not in BUDDYS:
        sock_remote.send(packet)
        buf = b''
        while len(buf) < 4:
            try:
                time.sleep(0.2)
                buf += sock_remote.recv(4 - len(buf))
            except WindowsError:
                pass
        length = struct.unpack('!I', buf)[0]

        text = sock_remote.recv(length)

        text = pickle.loads(text)

        if type(text) is join:
            tmp = Buddy(text.name, sock_remote, addr)
            BUDDYS.append(tmp)
            print(str(tmp.name) + " connected.")


def send_packet_server(packet, conn):
    packet = pickle.dumps(packet)
    length = struct.pack('!I', len(packet))
    packet = length + packet
    conn.send(packet)


start_new_thread(listen_all, ())


print("client starting")

while True:
    text = input("Command ? ('help' for Commands)\n")
    if text == "Q":
        for b in BUDDYS:
            send_packet_server(exit(), b.conn)
            b.conn.close()

        THREAD_RUNNING = False
        break
    elif text == "help":
            print("S------------Scan for Connections  \n")
            print("L------------List connected Buddys\n")
            print("C------------Send a Message to one   \n")
            print("Q------------Quit                                     \n")
            print("S------------Scan for Connections   \n")
            print("G------------Same as no Command         \n\n")

    elif text == "S":
        scan_open()
    elif text == "L":
        for b in BUDDYS:
            print("Buddy with name: " + str(b.name) + " has Address: " + str(b.addr) + "\n")
    elif text == "C":
        toWhichNickname = input("To which chat you wish to send a message ?\n")
        for b in BUDDYS:
            if toWhichNickname == b.name:
                msg = input("Enter your Message:\n")
                send_packet_server(message(msg), b.conn)
                break
    elif text == "G":
        print("Send Broadcast Message\n")
        msg = input("Please enter your message:\n")
        for b in BUDDYS:
            send_packet_server(message(msg), b.conn)
    else:
        print("None Command")
        continue
