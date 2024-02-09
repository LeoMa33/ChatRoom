import asyncio
from Client import Client

"""
 #//? MESSAGE TYPE :
    0 - Annonce
    1 - Message
    2 - Connection
    3 - Room

#//? ANNONCE TYPE :
    0 - NOUVELLE CONNECTION
    1 - DECONNECTION
"""


class Encoding:

    def encodeM(msgType=0, annonceType=0, pseudo="",color=0,msg="",roomName=""):

        if msgType == 0:
            annonceType = annonceType.to_bytes(1,'big')
            pseudo = pseudo.encode()
            pseudoLen = len(pseudo).to_bytes(1,'big')
            content = annonceType+pseudoLen+pseudo

        if msgType == 1:
            color=int(color).to_bytes(1,'big')
            pseudo = pseudo.encode()
            pseudoLen = len(pseudo).to_bytes(1,'big')
            msg = msg.encode()
            msgLen= len(msg).to_bytes(3,'big')
            content = color+pseudoLen+pseudo+msgLen+msg
        
        if msgType == 2:
            pseudo = pseudo.encode()
            pseudoLen = len(pseudo).to_bytes(1,'big')
            content = pseudoLen+pseudo

        if msgType == 3:
            pseudo = pseudo.encode()
            pseudoLen = len(pseudo).to_bytes(1,'big')
            roomName = roomName.encode()
            roomLen = len(roomName).to_bytes(1,'big')
            content = pseudoLen+pseudo+roomLen+roomName

        header = msgType.to_bytes(1,'big')

        return header+content


    async def decodeM(reader):
        header = await reader.read(1)

        if header == b'':
            return False
        
        msgType = int.from_bytes(header,'big')

        if msgType == 0:
            data = await reader.read(1)
            annonceType = int.from_bytes(data, 'big')
            
            data = await reader.read(1)
            pseudoLen = int.from_bytes(data,'big')

            data = await reader.read(pseudoLen)
            pseudo = data.decode()
            return(True, msgType, annonceType, pseudo)

        if msgType == 1:
            data = await reader.read(1)
            color = int.from_bytes(data, 'big')
            
            data = await reader.read(1)
            pseudoLen = int.from_bytes(data,'big')

            data = await reader.read(pseudoLen)
            pseudo = data.decode()

            data = await reader.read(3)
            msgLen = int.from_bytes(data, 'big')

            data = await reader.read(msgLen)
            msg = data.decode()
            return (True, msgType, color, pseudo, msg)

        if msgType == 2:
            data = await reader.read(1)
            pseudoLen = int.from_bytes(data,'big')

            data = await reader.read(pseudoLen)
            pseudo = data.decode()

            return (True, msgType, pseudo)
        
        if msgType == 3:
            data = await reader.read(1)
            pseudoLen = int.from_bytes(data,'big')

            data = await reader.read(pseudoLen)
            pseudo = data.decode()

            data = await reader.read(1)
            roomLen = int.from_bytes(data,'big')

            data = await reader.read(roomLen)
            roomName = data.decode()

            return (True, msgType, pseudo, roomName)
    
    async def sendAll(clients, msg,exception=[]):
        exception = [x.id for x in exception]
        for a,c in clients.items():
            c:Client
            if a in exception or not c._connection:continue
            c._writer.write(msg)
            await c._writer.drain()
