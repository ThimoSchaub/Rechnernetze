import socket, pickle, struct
from _thread import start_new_thread
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

window = Tk()
window.title("P2P_Group Chat")
out = scrolledtext.ScrolledText(window,width=40,height=10)
txt = Entry(window, width=30)
name = "T(h)imo"
def client():
    HOST = 'localhost'
    PORT = 50000
    # Create a socket connection.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    name = input("Insert name: ")
    packet = pickle.dumps(join(name))
    length = struct.pack('!I', len(packet))
    packet = length + packet
    s.send(packet)
    exit = False
    while not exit: 
        msg = input("Insert Message: ")
        packet = pickle.dumps(message(msg))
        length = struct.pack('!I', len(packet))
        packet = length + packet
        s.send(packet)
    s.close()
    print('Data Sent to Server')


def server_2():
    HOST = 'localhost'
    PORT = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
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
            out.insert= (name+":" + msg)
        # elif(type(data_variable) is exit):

        else:
            print("unknown message typ")
    conn.close()
    print(data_variable)
    # Access the information by doing data_variable.process_id or data_variable.task_id etc..,
    print('Data received from client')


def clicked():
    client()



def gui():

    out.grid(column=0,row=0,columnspan=2)


    txt.grid(column=0, row=1)
    btn = Button(window, text="Send", command=clicked)

    btn.grid(column=1, row=1)
    window.mainloop()



start_new_thread(server_2,())
#gui()
client()
# def start_server():
#
#
# def scan(s):
#
# def list(l):
#
# def chat(c):
#
# def group_chat(g):
#
# def quit(Q):
#
# s.send(message.encode('utf-8'))
# pickledResponse = s.recv(4096);
# response = pickle.loads(pickledResponse)
#
#
# response = pickle.loads(pickledResponse)
# EOFError: Ran out of input
