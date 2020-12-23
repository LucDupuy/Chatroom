import socket
import threading

# HOST = 0.0.0.0
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048


clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))



def send_data_to_select_people(msg, idx):
    for client in clients:
     #   if clients.index(client) != idx:
            client.send(msg)


def handle(client):
    while True:
        try:
            data = client.recv(BUFFER_SIZE)
            send_data_to_select_people(data, clients.index(client))
        except socket.error:
            client_idx = clients.index(client)
            del clients[client_idx]
            client.close()
            break

def server():
    while True:
        try:
            client, address = s.recvfrom(BUFFER_SIZE)
            clients.append(client)
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except socket.error as e:
            print("Receiving: ", e)
            pass






if __name__ == '__main__':
    server()

# TODO: Currently this is TCP, not UDP
# TODO: Deal with multiple clients
# TODO: Server should not have mic in, it should only receive and send
