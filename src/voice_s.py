import socket

HOST = '0.0.0.0'
#HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((HOST, PORT))

clients = []

while True:
    try:
        msg, addr = server_sock.recvfrom(BUFFER_SIZE)
        clients.append(addr)
        print("Connected: ", addr)
    except socket.error:
        pass

    for client in clients:
      if client != addr:
        server_sock.sendto(msg, client)


# TODO: Remove client when they leave