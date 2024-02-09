import asyncio
import logging
import argparse
import sys
from configparser import ConfigParser
from aioconsole import ainput
from print_color import print
from ascii_magic import AsciiArt
from Encoding import Encoding

configFile = open('./config/client.conf')
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

logging.basicConfig(level=logging.DEBUG ,filename="./log/chat_server/client.log", filemode="w", format='%(asctime)s %(levelname)s %(message)s')


SERVER_UP = False

COLORS= {
    0:"purple",
    1:"blue",
    2:"green",
    3:"yellow",
    4:"red",
    5:"magenta",
    6:"cyan"
}

pseudo = ""

inputMode = "TEXT"

async def async_input(writer:asyncio.StreamReader):
    global inputMode
    global SERVER_UP
    while SERVER_UP:
        print(f"{inputMode} :")
        msg = await ainput("")
        print("\033[F\033[K", end="")
        print("\033[F\033[K", end="")
        if msg == "":continue

        if msg == "UPLOAD":
            inputMode = "UPLOAD"
            continue

        if msg == "TEXT":
            inputMode = "TEXT"
            continue
        
        if inputMode == "UPLOAD":
            msg = AsciiArt.from_image(msg).to_ascii()

        logging.info(f"MSG | FROM : Vous | CONTENT : {msg}")
        print(f"\n{msg}\n", tag="Vous", tag_color="white", color="white")
        
        msg = Encoding.encodeM(msgType=1,pseudo=pseudo, color=0, msg=msg)
        writer.write(msg)
        await writer.drain()

async def async_receive(reader:asyncio.StreamReader):
    global SERVER_UP
    while SERVER_UP:
        data = await Encoding.decodeM(reader)
        
        print("\033[F\033[K", end="")

        if not data[0]:
            print("Server closed")
            SERVER_UP = False
            break

        if data[1] == 1:
            logging.info(f"MSG | FROM : {data[3]} | CONTENT : {data[4]}")
            print(f"\n{data[4]}\n", tag=data[3], tag_color=COLORS[data[2]], color="white")

        if data[1] == 0:
            if data[2] == 0:
                print(f"{data[3]} a rejoint la room\n", tag="ANNONCE", tag_color="green",color="green")
                logging.info(f"ANNONCE | CONTENT : {data[3]} a rejoint la room")
            if data[2] == 1:
                print(f"{data[3]} a quitté la room\n", tag="ANNONCE", tag_color="red", color="red")
                logging.info(f"ANNONCE | CONTENT : {data[3]} a quitté la room")

        print(f"{inputMode} :")

async def main():
    global SERVER_UP
    global pseudo

    pseudo = input("Choisir un pseudo : ")
    logging.info(f"CONFIGURATION | PSEUDO : {pseudo}")
    print(chr(27) + "[2J")
    reader, writer = await asyncio.open_connection(host=host, port=port)
    logging.info(f"CONNECTION | HOST : {host} | PORT : {port}")
    writer.write(Encoding.encodeM(msgType=2,pseudo=pseudo))
    await writer.drain()
    SERVER_UP = True
    await asyncio.gather(async_input(writer=writer), async_receive(reader=reader))
    writer.close()
    await writer.wait_closed()

if __name__=="__main__":
    asyncio.run(main())
