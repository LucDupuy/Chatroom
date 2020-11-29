import socket
import threading
import tkinter.messagebox

HOST = socket.gethostbyname("ilkka.ddns.net")
PORT = 1127
BUFFER_SIZE = 1024

# IPV4, TCP
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_sock.connect((HOST, PORT))
except:
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.withdraw()
    tkinter.messagebox.showinfo("Error", "Server is offline")
    exit(0)
username = input("Please enter your username: ")


def client():
    while True:
        try:
            msg = server_sock.recv(BUFFER_SIZE).decode()
            if msg == "USERNAME":
                server_sock.send(username.encode())
            else:
                # Seeing what the server has to say
                print(msg)
        except:
            print("Server has gone offline.")
            server_sock.close()
          #  exit(0)
            break


def send_data():
    while True:
        msg = username + ": " + input()
        server_sock.send(msg.encode())


read_thread = threading.Thread(target=client)
read_thread.start()

write_thread = threading.Thread(target=send_data)
write_thread.start()
