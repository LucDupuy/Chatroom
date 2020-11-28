import socket
import threading

HOST = socket.gethostname()
PORT = 1127
BUFFER_SIZE = 1024

# IPV4, TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
username = input("Please enter your username: ")



def client():
    while True:
        try:
            msg = client.recv(BUFFER_SIZE).decode()
            if msg == "USERNAME":
                client.send(username.encode())
            else:
                # Seeing what the server has to say
                print(msg)
        except:
            print("Error occurred.")
            client.close()
            break




def send_data():

    while True:
        msg = f'{username}: {input()}'
        client.send(msg.encode())


read_thread = threading.Thread(target=client)
read_thread.start()

write_thread = threading.Thread(target=send_data)
write_thread.start()