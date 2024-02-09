import asyncio
import random

class Client:
    def __init__(self, addr:(str,int), pseudo:str, reader:asyncio.StreamReader, writer:asyncio.StreamWriter):
        self._ip = addr[0]
        self._port = addr[1]
        self._reader = reader
        self._writer = writer
        self._color = random.randint(0,6)
        self._pseudo = pseudo
        self._connection = True
    
    @property
    def id(self):
        return hash(f"{self._ip}:{self._port}:{self._pseudo}")