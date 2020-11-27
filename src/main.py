import socket

HOST = socket.gethostname()
PORT = 1234
NUM_CONNECTIONS = 3
BUFFER_SIZE = 1024


def server():
    # IPV4, TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((HOST, PORT))
    s.listen(NUM_CONNECTIONS)

    while True:
        client, address = s.accept()
        print(address[0], "has joined on port:", address[1])

        received_data(client.recv(BUFFER_SIZE))

        data = "Thank you for connecting to my server"
        send_data(data, client=client)


def send_data(data, client):
    # Encode turns the string into bytes
    client.send(data.encode())
    client.close()


def received_data(data):
    print(data)


if __name__ == '__main__':
    server()
