import socket

HOST = '0.0.0.0'
# HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
BUFFER_SIZE = 2048


def main():
    """
    Collects the voice data from users and sends it back to everyone
    """

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((HOST, PORT))

    while True:
        try:
            data, address = server_sock.recvfrom(BUFFER_SIZE)
            server_sock.sendto(data, address)
            # print(data)
        except socket.error as e:
            print(e)
            server_sock.close()
            exit(0)


if __name__ == '__main__':
    main()
