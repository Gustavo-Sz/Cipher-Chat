import socket
import threading
from _thread import allocate_lock
from crip import cryptography
import time
from chatcmds import cmds

ip = "192.168.1.15"
addr = (ip, port)
port 9192


class Channel():

    def __init__(self, target_key, client_socket, destine):
        self.my_publickey = cryptography.getfromfile()
        self.app_socket = client_socket
        self.destine = destine
        self.cript = cryptography(target_key)


def sendmsg(channel):

    t2 = threading.Thread(target=receive, args=(channel,), daemon=True)
    t2.start()
    print("\n[Client] Whenever you want, type '/channel desconnect' to leave this conversation.\n")
    while True:
        msg = input()

        if msg == "/channel desconnect":
            msg = cmd["chChange"]
            size = f"{len(msg):<10}".encode('utf-8')
            channel.app_socket.send(size + msg)

            print("\n[Client] Type user's id to start conversation:\n")
            target_identifier = input("> ")

            # Destine / target_identifier
            msg = cmds().newDestine(target_identifier)
            size = f"{len(msg):<10}".encode('utf-8')
            client_socket.send(size + msg)

        elif msg == "/server desconnect":
            msg = cmd["svDesconnect"]
            size = f"{len(msg):<10}".encode('utf-8')
            channel.app_socket.send(size + msg)
            break

        else:
            msgcipher = channel.cript.encryptmsg(msg.encode('utf-8'))
            size = f"{len(msgcipher):<10}".encode('utf-8')
            full_msg = size + msgcipher
            channel.app_socket.send(full_msg)

        time.sleep(0.1)
    t2.join()


def receive(channel):

    while True:
        msgsize = cmds.getHeaderSize(channel.app_socket)

        msgcontent = channel.app_socket.recv(msgsize)

        if cmd["dstKey"] in msgcontent:
            Lock = allocate_lock()
            msgcontent = msgcontent.strip(cmd["dstKey"])  # SIZEDESTINE DESTINE KEY
            sizeDestine = msgcontent[:10]
            msgcontent = msgcontent.strip(sizeDestine)  # DESTINE KEY
            msgdestine = msgcontent[:int(sizeDestine.decode('utf-8'))]
            key = msgcontent.strip(msgdestine)  # KEY
            Lock.acquire()
            channel.cript = cryptography(key)
            Lock.release()
            Lock.acquire()
            channel.destine = msgdestine.decode('utf-8')
            Lock.release()

        elif cmd["svDesconnect"] == msgcontent:
            msg = cmd["svDesconnect"]
            size = f"{len(msg):<10}".encode('utf-8')
            channel.app_socket.send(size + msg)
            print("[App] Desconnecting from server...")
            break

        elif cmd["dstNotFound"] == msgcontent:
            print("\n[Client] Client not found. Type another username to start conversation:\n")
            target_identifier = input("> ")
            # Destine / target_identifier
            msg = cmds().newDestine(target_identifier)
            size = f"{len(msg):<10}".encode('utf-8')
            client_socket.send(size + msg)

        else:
            plaintext = channel.cript.decryptmsg(msgcontent)
            print(f"{channel.destine} : {plaintext}")


def app(client_socket, desconnect, identifier):

    print("\n[Client] Choose a name to be your id: \n")
    identifier = input("> ")
    identifier += "-"
    identifier = identifier.encode('utf-8')

    # Identifier
    msg = identifier + cryptography.getfromfile()
    size = f"{len(msg):<10}".encode('utf-8')
    client_socket.send(size + msg)

    print("\n[Client] Now, you can type '/server desconnect' anytime in order to desconnect from the server.\n")

    while not desconnect:
        print("\n[Client] Type user's id to start conversation:\n")
        target_identifier = input("> ")

        # Destine / target_identifier

        if target_identifier != "/server desconnect":
            client_socket.send(bytes(f"{len(target_identifier):<10}{target_identifier}", 'utf-8'))
            # Resultado pesquina destine

            msgsize = cmds.getHeaderSize(client_socket)

            key = client_socket.recv(msgsize)

            if key.decode('utf-8') != "ClientNotFound":
                global channel
                channel = Channel(key, client_socket, target_identifier)
                sendmsg(channel)
                client_socket.close()
                desconnect = True
            else:
                print("\n[Client] User not found.\n")

        else:
            msg = cmd["svDesconnect"]
            size = f"{len(msg):<10}".encode('utf-8')
            client_socket.send(size + msg)

            msgsize = cmds.getHeaderSize(client_socket)

            msgcontent = client_socket.recv(msgsize).decode('utf-8')
            if msgcontent == cmd["svDesconnect"]:
                print("[App] Desconnected from server. Restart the application to reconnect.")
                desconnect = True


cmd = cmds().commands
desconnect = True
tries = 0

while desconnect & (tries < 10):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(addr)
        desconnect = False
        app(client_socket, desconnect, identifier)
        tries = 0

    except ConnectionRefusedError:
        tries += 1
        print("\n[Client] Couldn't connect to the server. Trying again...\n")

        if tries == 10:
            print("\n[Client] Multiple connection attempts failed. Try later.\n")
