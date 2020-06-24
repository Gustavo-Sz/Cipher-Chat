class cmds():
    def __init__(self):
        self.commands = {"svDesconnect": b"---COMMAND---DESCONNECTSERVER","chChange": b"---COMMAND---CHANNELCHANGE", "dstIdentifier": b"---ACTION---DESTINECHANGE----", "dstKey": b"---INFO---DESTINEKEY----", "dstNotFound": b"---ACTIONERROR---DESTINENOTFOUND"}

    def newDestine(self, destine):
        return self.commands["dstIdentifier"] + destine.encode()

    def sendDestineKey(self, destine, key):
        # SIZE dstKey SIZEDESTINE DESTINE KEY
        sizeDestine = f"{len(destine):<10}".encode("utf-8")
        protocol = self.commands["dstKey"] + sizeDestine + destine.encode('utf-8') + key
        return protocol

    @staticmethod
    def getHeaderSize(socket):
        msg = False
        while not msg:
            try:
                size_msg = socket.recv(10).decode('utf-8')
                size_msg = int(size_msg)
                msg = True

            except ValueError:
                msg = False

            except ConnectionError:
                print(f"[Server] Conexão perdida com {socket.getpeername()}")
        return size_msg
