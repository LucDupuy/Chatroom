import socket

HOST = socket.gethostname()
PORT = 1127
BUFFER_SIZE = 1024


def client():
    USER = input("Enter your username: ")

    server_socket = setup(username=USER)


    while True:
        user_input = input(USER + ": ")
        data = USER + ": " + user_input

        send_data(data, server=server_socket)
        received_data(server_socket.recv(BUFFER_SIZE))


def setup(username):

    # IPV4, TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    data = username + ": Hello Server"
    send_data(data, server=s)
    received_data(s.recv(BUFFER_SIZE))

    return s


def send_data(data, server):
    # Encode turns the string into bytes
    server.send(data.encode())


def received_data(data):
    print(data.decode())


if __name__ == '__main__':
    client()
