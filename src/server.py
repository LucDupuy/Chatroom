import socket
import threading
from datetime import datetime
import voice_s as vs
from threading import Thread

# HOST = 0.0.0.0
HOST = socket.gethostbyname("ROGUEONE")
PORT = 1127
NUM_CONNECTIONS = 5
BUFFER_SIZE = 1024
DATETIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

clients = []
usernames = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(NUM_CONNECTIONS)
print("\n\n" + DATETIME)
print("--------------------")
print("\nServer listening.....")


def send_data_to_select_people(msg, idx, only_current):
    for client in clients:
        if only_current:
            if clients.index(client) == idx:
                client.send(msg)
        else:
            if clients.index(client) != idx:
                client.send(msg)


def send_data(msg):
    for client in clients:
        client.send(msg)


def handle(client):
    while True:
        try:
            data = client.recv(BUFFER_SIZE)
            if data.decode().__contains__("#users"):
                send_data_to_select_people(list_online().encode(), clients.index(client), only_current=True)
            elif data.decode().__contains__("#voice"):
                send_data_to_select_people("VOICE".encode(), clients.index(client), only_current=True)

                voice_thread = Thread(target=vs.main)
                voice_thread.start()

            elif data.decode().__contains__("#stop_voice"):
                send_data_to_select_people("STOP_VOICE".encode(), clients.index(client), only_current=True)

            elif data.decode().__contains__("#help"):
                send_data_to_select_people(list_commands().encode(), clients.index(client), only_current=True)

            else:
                send_data_to_select_people(data, clients.index(client), only_current=False)
        except:
            client_idx = clients.index(client)
            del clients[client_idx]
            client.close()
            username = usernames[client_idx]
            data = f'{username} left the chat.'

            send_data(data.encode())
            del usernames[client_idx]
            break


def server():
    while True:
        try:
            client, address = s.accept()
            client.send("USERNAME".encode())
        except:
            TIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print("Keyboard Interruption: Server closing.\n" + TIME)
            s.close()
            exit(0)
        try:
            username = client.recv(1024).decode()
            usernames.append(username)
        except:
            print("User closed connection")
            continue

        clients.append(client)

        send_data(f"{username} has joined the chat.".encode())
        send_data_to_select_people(list_online().encode(), clients.index(client), only_current=True)
        send_data_to_select_people("Type #help for options\n".encode(), clients.index(client), only_current=True)


        thread = threading.Thread(target=handle, args=(client,))
        thread.daemon = True
        thread.start()


def list_online():
    data = ""
    data += "\nUsers Currently Online\n"
    data += "**********************\n"
    for username in usernames:
        data += username + "\n"

    return data




def list_commands():
    data = ""
    data += "\n#users -> List the users currently online"
    data += "\n#voice -> Join the voice chat"
    data += "\n#stop_voice -> Leave the voice chat\n"

    return data


if __name__ == '__main__':
    server()

# TODO: Implement Voice -> REMOVE ALL UDP FROM HERE AND USE SEPARATE PROGRAM
# TODO: How to push updates?
# TODO: Message from another shouldn't interrupt your typing
# TODO: Suppress not a trusted source from windows
