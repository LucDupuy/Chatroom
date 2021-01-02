import socket
from threading import Thread
import tkinter.messagebox
import voice_c as vc
import subprocess
from multiprocessing import Process
import sys

# HOST = socket.gethostbyname("ilkka.ddns.net")
HOST = socket.gethostbyname("ROGUEONE")
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

            elif msg == "VOICE":


            else:
                # Seeing what the server has to say
                print(msg)
        except socket.error:
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


read_thread = Thread(target=client)
read_thread.start()

write_thread = Thread(target=send_data)
write_thread.start()
