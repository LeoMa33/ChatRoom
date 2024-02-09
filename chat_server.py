import asyncio
import logging
import argparse
import sys
from configparser import ConfigParser
from Client import Client
from Encoding import Encoding

configFile = open('./config/server.conf')
config = ConfigParser(allow_no_value=True)
config.read_string(configFile.read())

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", action="store", default=int(config["DEFAULT"]["PORT"]), type=int, help="choice a port beetween : 0 and 65535")
parser.add_argument("-a", "--address", action="store", default=config["DEFAULT"]["HOST"], type=str, help="choice server host")
args = parser.parse_args()

configFile.close()

host=args.address
port=args.port

if 0 > port or port > 65535:
    print("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
    sys.exit(1)
if 0<= port <= 1024:
    print("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
    sys.exit(2)

logging.basicConfig(level=logging.DEBUG ,filename="./log/chat_server/server.log", filemode="w", format='%(asctime)s %(levelname)s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

CLIENTS = {}
ROOMS = {}

async def handle_client_msg(reader:asyncio.StreamReader, writer:asyncio.StreamWriter):
    global CLIENTS
    while True:
        data = await Encoding.decodeM(reader)
        addr = writer.get_extra_info('peername')

        if not data:
            msg = Encoding.encodeM(msgType=0,annonceType=1,pseudo=client._pseudo)
            logging.info(f"{client._ip}:{client._port} : {client._pseudo} disconnected")
            client._connection = False

        elif data[1] == 2:
            client = Client(addr=addr,pseudo=data[2], reader=reader,writer=writer)
            if client.id in CLIENTS.keys():
                writer.write("Welcome back !")
                client:Client = CLIENTS[client.id]
                client._connection = True
                logging.info(f"New connection from {client._ip}:{client._port} : {client._pseudo}")
                
                msg = Encoding.encodeM(msgType=0,annonceType=0,pseudo=client._pseudo)
            else:
                CLIENTS[client.id] = client
                logging.info(f"New connection from {client._ip}:{client._port} : {client._pseudo}")

                
                msg = Encoding.encodeM(msgType=0,annonceType=0,pseudo=client._pseudo)
        else:

            logging.info(f"Message received from {addr[0]}:{addr[1]} : {data[4]}")
            msg = Encoding.encodeM(msgType=1,pseudo=client._pseudo, color=client._color, msg=data[4])

        await Encoding.sendAll(CLIENTS, msg, [client])

        if not data: break


async def main():

    server = await asyncio.start_server(handle_client_msg, host, port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    logging.info(f"Le serveur tourne sur {addrs}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
