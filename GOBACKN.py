from lossy_udp_socket import lossy_udp_socket
from socket import *

HOST = gethostbyname(gethostname())
PORT = 5000

def startlossy():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))
    (conn, addr) = sock.accept()
    sock = lossy_udp_socket(conn,5000,addr,0)
    sock.send(b'test')
    msg = sock.recv()
    print(msg)

def send(msg):
    print(msg)


if __name__ == '__main__':
    startlossy()
    #sendloosy()
