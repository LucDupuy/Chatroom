import socket

HOST = socket.gethostname()
PORT = 1234
BUFFER_SIZE = 1024


def client():
    # IPV4, TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.send(send_data())
    received_data(s.recv(BUFFER_SIZE))

    s.close()


def send_data():
    data = "Hello Server"
    return data.encode()


def received_data(data):

    print(data.decode())


if __name__ == '__main__':
    client()
