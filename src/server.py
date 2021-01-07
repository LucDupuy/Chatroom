import socket
import threading
from datetime import datetime
import voice_s as vs
from threading import Thread

# HOST = 0.0.0.0
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
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
    """
    Sends data to certain people depending on if only the current user needs to
    see the information or if everyone should see it
    :param msg: the message to be sent
    :param idx: the index of the current client in the clients list
    :param only_current: if we only want to send the message to the current user or not
    """

    for client in clients:
        if only_current:
            if clients.index(client) == idx:
                client.send(msg)
        else:
            if clients.index(client) != idx:
                client.send(msg)


def send_data(msg):
    """
    Send data to all the connected clients
    :param msg: the message to send
    """
    for client in clients:
        client.send(msg)


def handle(client, event):
    """
    Depending on the information recieved from the client, the server will decide to send it
    to certain people
    :param client: the current client
    :param event: the event handler for the main thread of the server
    """

    while event.is_set():
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

            elif data.decode().__contains__("#mute"):
                send_data_to_select_people("MUTE".encode(), clients.index(client), only_current=True)

            elif data.decode().__contains__("#exit"):
                send_data_to_select_people("EXIT".encode(), clients.index(client), only_current=True)
                remove_client(client)
                break

            else:
                send_data_to_select_people(data, clients.index(client), only_current=False)
        except socket.error:
            idx = clients.index(client)
            user = usernames[idx]
            print(f"{user} forcibly disconnected")
            remove_client(client)
            break


def server():
    """
    Initialize the main server and accept clients.
    Initialize the thread for the handling the clients and their messages.
    """
    while True:
        try:
            client, address = s.accept()
            client.send("USERNAME".encode())
        except socket.error as e:
            TIME = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print("Keyboard Interruption: Server closing.\n" + TIME)
            print("\n", e, "\n")
            s.close()
            exit(0)
        try:
            username = client.recv(1024).decode()
            usernames.append(username)
        except socket.error as e:
            print(e, "\n")
            print("User closed connection")
            continue

        clients.append(client)

        send_data(f"{username} has joined the chat.".encode())
        send_data_to_select_people(list_online().encode(), clients.index(client), only_current=True)
        send_data_to_select_people("Type #help for options\n".encode(), clients.index(client), only_current=True)


        server_thread_event = threading.Event()
        server_thread_event.set()

        thread = threading.Thread(target=handle, args=(client, server_thread_event))
        thread.daemon = True
        thread.start()


def list_online():
    """
    Lists the users currently online
    :return: the string of users
    """
    data = ""
    data += "\nUsers Currently Online\n"
    data += "**********************\n"
    for username in usernames:
        data += username + "\n"

    return data


def list_commands():
    """
    Lists the commands that the user can use
    :return: the string of commands
    """
    data = ""
    data += "\n#users -> List the users currently online"
    data += "\n#voice -> Join the voice chat"
    data += "\n#stop_voice -> Leave the voice chat"
    data += "\n#exit -> Exit the voice chat"
    data += "\n#mute -> Mute and unmute yourself"

    return data


def remove_client(client):
    """
    Removes a client from the server
    :param client: the client to remove
    """
    client_idx = clients.index(client)
    del clients[client_idx]
    client.close()
    username = usernames[client_idx]
    data = f'{username} left the chat.'

    send_data(data.encode())
    del usernames[client_idx]


if __name__ == '__main__':
    server()
