import socket
import tkinter.messagebox
import voice_c as vc
from esky import *
import requests
import webbrowser


"""
Prompts the user to update the app if an update is available
"""
###################################################################################################
VERSION = "1.0"

response = requests.get("https://ilkka.ddns.net/LukiChat/version.txt")
data = response.text

print("Checking for update...")
if data > VERSION:
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.withdraw()
    response = tkinter.messagebox.askyesno("Update", "Update available, would you like to download?")

    if response:
        webbrowser.open("https://ilkka.ddns.net/LukiChat/")
    else:
        pass

else:
    print("No Update")
    pass
###################################################################################################


#HOST = socket.gethostbyname("ilkka.ddns.net")
HOST = socket.gethostbyname("Thanos")
PORT = 80
BUFFER_SIZE = 1024

VOICE_BOOL = False
MUTE_BOOL = False

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
Checks to see if the server is online to connect to
"""
try:
    server_sock.connect((HOST, PORT))
except socket.error:
    root = tkinter.Tk()
    root.overrideredirect(1)
    root.withdraw()
    tkinter.messagebox.showinfo("Error", "Server is offline")
    exit(0)

username = input("Please enter your username: ")


def client(event):
    """
    Handles messages from the  server and starts the voice chat when prompted
    :param event: the event used to gracefully kill threads
    """

    while event.is_set():
        try:
            msg = server_sock.recv(BUFFER_SIZE).decode()
            if msg == "USERNAME":
                server_sock.send(username.encode())

            elif msg == "VOICE":
                global VOICE_BOOL
                if not VOICE_BOOL:
                    get_event, send_event, get_thread, send_thread = vc.main()
                    VOICE_BOOL = True
                else:
                    pass
            elif msg == "STOP_VOICE":
                get_event.clear()
                send_event.clear()
                get_thread.join()
                send_thread.join()
                VOICE_BOOL = False

            elif msg == "MUTE":

                print("Muting and unmuting is not yet supported.")

            elif msg == "EXIT":
                print("You have disconnected from the server")
                read_event.clear()
                write_event.clear()
                server_sock.close()
                exit(0)

            else:
                # Seeing what the server has to say
                print(msg)
        except socket.error as e:
            print(e)
            server_sock.close()
            exit(0)


def send_data(event):
    """
    Sends messages to the server and checks to see if it has gone offline
    :param event: the event used to gracefully kill threads
    """

    while event.is_set():
        try:
            msg = username + ": " + input()

            if len(msg) > (len(username) + 2):
                server_sock.send(msg.encode())
        except socket.error as e:
            server_sock.close()
            print(e, "\n")
            print("Server has gone offline")
            exit(0)


"""
Starts the threads for sending and receiving data, as well as
the events needed to kill the threads
"""
read_event = threading.Event()
read_event.set()

write_event = threading.Event()
write_event.set()

read_thread = threading.Thread(target=client, args=(read_event,))
read_thread.start()

write_thread = threading.Thread(target=send_data, args=(write_event,))
write_thread.start()
