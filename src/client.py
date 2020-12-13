import socket
import threading
import tkinter.messagebox
import voice_c as vc

# HOST = socket.gethostbyname("ilkka.ddns.net")
HOST = socket.gethostbyname("ROGUEONE")
PORT = 80
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

            elif msg == "VOICE":
               vc.client()

            else:
                # Seeing what the server has to say
                print(msg)
        except:
            server_sock.close()
            exit(0)


def send_data():
    while True:
        try:
            msg = username + ": " + input()
            if len(msg) > (len(username) + 2):
                server_sock.send(msg.encode())
        except:
            server_sock.close()
            print("Server has gone offline")
            exit(0)



read_thread = threading.Thread(target=client)
read_thread.start()

write_thread = threading.Thread(target=send_data)
write_thread.start()
