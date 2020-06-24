from database import databaseClass


class dbHelper():

    def __init__(self):
        self.__db = databaseClass()

    def close(self):
        self.__db.closedb()

    def addClient(self, identifier, key):
        if not self.__checkExistence(identifier):
            self.__db.insert("clients", (identifier, key))

    def remClient(self, identifier):

        self.__db.delete("clients", ("id", identifier))

    def getpublickey(self, destine):

        if self.__checkExistence(destine):
            key = self.__db.get("clients", ("pk",), ("id", destine))
            return key[0][0]
        else:
            return False

    def __checkExistence(self, identifier):

        result = self.__db.get("clients", ("id",), ("id", identifier))
        if len(result) != 0:
            return True
        else:
            return False

    def getMessages(self, identifier, source):

        msg = self.__db.get("messages", ("id","source", "content"), ("destination", identifier, "source", source))
        for x in msg:
            self.__db.delete("messages", ("id", x[0]))
        return msg

    def insertMessage(self, identifier, destination, message):

        self.__db.insert("messages", (None, identifier, destination, message))

    def getOnlineClients(self):
        strClients = ""
        clients = self.__db.get("clients", ("id",), ())
        if len(clients) > 0:
            for x in clients:
                strClients += f"{x} \n"
            return strClients
        else : 
            return "Não há usuários online"
