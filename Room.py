from Client import Client


class Room:
    def __init__(self, name):
        self.CLIENTS = {}
        self.name = name
    
    def addClient(self, key:str, client:Client):
        self.CLIENTS[key] = client
    
    def removeClient(self, key):
        del self.CLIENTS[key]