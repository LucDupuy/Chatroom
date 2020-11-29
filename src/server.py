import socket
import threading

HOST = "0.0.0.0"
PORT = 1127
NUM_CONNECTIONS = 5
BUFFER_SIZE = 1024

clients = []
usernames = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(NUM_CONNECTIONS)
print("Server listening......")


def send_data_to_all_but_current(msg, idx):
    for client in clients:
        if clients.index(client) == idx:
            client.send(msg)


def send_data(msg):
    for client in clients:
        client.send(msg)


def handle(client):
    while True:
        try:
            data = client.recv(BUFFER_SIZE)
            send_data(data)
        except:
            client_idx = clients.index(client)
            del clients[client_idx]
            client.close()
            username = usernames[client_idx]
            data = f'{username} left the chat.'
            print(f'{username} disconnected from the server.')
            send_data(data.encode())
            del usernames[client_idx]
            break


def server():
    while True:
        client, address = s.accept()
        client.send("USERNAME".encode())
        try:
            username = client.recv(1024).decode()
            usernames.append(username)
        except:
            print("User closed connection")

        clients.append(client)
        print("Number of Users Connected: ", len(clients))
        print(f"{username} has connected.")

        send_data(f"{username} has joined the chat.".encode())

        send_data_to_all_but_current(list_online().encode(), clients.index(client))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def list_online():
    data = ""
    data += "\nUsers Currently Online\n"
    data += "**********************\n"
    for username in usernames:
        data += username + "\n"

    return data


if __name__ == '__main__':
    server()

# Message to not display twice
# Message from another shouldn't interrupt your typing
# Handle exception when server closes and user still on
