import socket
import threading
import tkinter.messagebox
import voice_c as vc

# HOST = socket.gethostbyname("ilkka.ddns.net")
HOST = socket.gethostbyname("ROGUEONE")
PORT = 1127
BUFFER_SIZE = 1024

VOICE_BOOL = False

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

#username = input("Please enter your username: ")
username = "Luc"


def client(event):
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
    while event.is_set():
        try:
            msg = username + ": " + input()
            if len(msg) > (len(username) + 2):
                server_sock.send(msg.encode())
        except socket.error as e:
            server_sock.close()
            print("Server has gone offline")
            exit(0)



read_event = threading.Event()
read_event.set()

write_event = threading.Event()
write_event.set()

read_thread = threading.Thread(target=client, args=(read_event, ))
read_thread.start()

write_thread = threading.Thread(target=send_data, args=(write_event, ))
write_thread.start()
