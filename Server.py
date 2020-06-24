import socket
from dbcmds import dbHelper
import threading
from _thread import allocate_lock
import time
from chatcmds import cmds

ip = "192.168.1.15"
port = 9192
connections = 2
addr = (ip, port)

print("[Server] Starting server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(addr)
server_socket.listen(connections)
print("[Server] Server connections open.")
print("[Server] Searching for new connections..")


class Clienthandle():

    def __init__(self, clientsocket, addr):

        self.clientsocket = clientsocket
        self.clientaddr = addr
        self.publickey_destine = b""
        self.destine = ""
        self.identifier = ""
        self.serverdesconectar = False

    def receive(self):
        while True:
            db = dbHelper()

            size_msg = cmds.getHeaderSize(self.clientsocket)

            msgcontent = self.clientsocket.recv(size_msg)

            if msgcontent == cmd["chChange"]:
                print(f"[Server] Client {self.identifier} changing destination.")

                size_msg = cmds.getHeaderSize(self.clientsocket)

                msgcontent = self.clientsocket.recv(size_msg)

                if cmd["dstIdentifier"] in msgcontent:
                    Lock = allocate_lock()
                    Lock.acquire()
                    self.destine = msgcontent.strip(cmd["dstIdentifier"]).decode('utf-8')
                    Lock.release()

                    Lock.acquire()
                    self.publickey_destine = db.getpublickey(self.destine)
                    Lock.release()

                    if self.publickey_destine:
                        msg = cmds().sendDestineKey(self.destine, self.publickey_destine)

                    else:
                        msg = cmd["dstNotFound"]

                    size = f"{len(msg):<10}".encode('utf-8')
                    self.clientsocket.send(size + msg)

            elif msgcontent == cmd["svDesconnect"]:
                print(f"[Server] Client {self.identifier} desconnecting from server.")
                msg = cmd["svDesconnect"]
                size = f"{len(msg):<10}".encode('utf-8')
                self.clientsocket.send(size + msg)
                break

            else:
                db.insertMessage(self.identifier, self.destine, msgcontent)

    def sendmsg(self):
        db = dbHelper()

        while True:

            if self.destine != "":
                msgs = db.getMessages(self.identifier, self.destine)

                for x in msgs:
                    msg = x[2]
                    size = f"{len(msg):<10}".encode('utf-8')
                    full_msg = size + msg
                    self.clientsocket.send(full_msg)
                    time.sleep(0.1)

    def run(self):
        self.serverdesconectar = False
        t1 = threading.Thread(target=self.receive)
        t2 = threading.Thread(target=self.sendmsg)
        t1.start()
        t2.start()
        t1.join()
        self.clientsocket.close()


def run_client(clientinfos, index):
    clientclass = Clienthandle(clientinfos[0], clientinfos[1])
    db = dbHelper()
    # identifier

    size_msg = cmds.getHeaderSize(clientclass.clientsocket)

    client_info = clientclass.clientsocket.recv(size_msg)

    clientclass.identifier = client_info[:client_info.find(b"-")].decode()

    key = client_info[client_info.find(b"-")+1:]

    db.addClient(clientclass.identifier, key)

    while True:
        clientclass.destine = ""
        clientclass.publickey_destine = ""
        key = ""
        # Destine identifier

        size_msg = cmds.getHeaderSize(clientclass.clientsocket)

        destine = clientclass.clientsocket.recv(size_msg).decode('utf-8')

        if destine == "/server desconnect":
            clientclass.serverdesconectar = True
            msg = cmd["svDesconnect"]
            size = f"{len(mds):<10}".encode('utf-8')
            clientclass.clientsocket.send()

        else:
            key = db.getpublickey(destine)

            if key:
                clientclass.destine = destine
                clientclass.publickey_destine = key

                size = f"{len(key):<10}".encode('utf-8')
                msg = size + key
                clientclass.clientsocket.send(msg)

                clientclass.run()
                break
            else:
                warningmsg = "ClientNotFound"
                clientclass.clientsocket.send(bytes(f"{len(warningmsg):<10}{warningmsg}", 'utf-8'))

    clientclass.clientsocket.close()
    Lock = allocate_lock()
    Lock.acquire()
    sockets.pop(index)
    Lock.release()


index = 0
global sockets
sockets = {}
cmd = cmds().commands
while True:
    clientsocket, client_addrs = server_socket.accept()
    print(f"New client connected: {client_addrs}")
    clientinfos = (clientsocket, client_addrs)
    sockets[index] = threading.Thread(target=run_client, args=(clientinfos, index))
    sockets[index].start()
    index += 1
