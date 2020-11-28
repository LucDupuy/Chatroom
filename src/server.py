import socket
from pynput.keyboard import Key, Listener

HOST = socket.gethostname()
PORT = 1127
NUM_CONNECTIONS = 3
BUFFER_SIZE = 1024


def server():
    USER = input("Enter your username: ")

    # IPV4, TCP

    client, address = setup(username=USER)


    while True:
        user_input = input(USER + ": ")
        data = USER + ": " + user_input
        send_data(data, client=client)

        received_data(client.recv(BUFFER_SIZE))


def setup(username):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(NUM_CONNECTIONS)
    client, address = s.accept()
    print(address[0], "has joined")
    received_data(client.recv(BUFFER_SIZE))
    data = username + ": Thank you for connecting to my server"
    send_data(data, client=client)

    return client, address


def send_data(data, client):
    # Encode turns the string into bytes

    client.send(data.encode())


def received_data(data):
    print(data.decode())


if __name__ == '__main__':
    server()
