from threading import Thread
from time import time
from binascii import unhexlify

class TcpTest(Thread):
    def __init__ (self, s, buffer_size,direction):
        Thread.__init__(self)
        self.sock = s
        self.buffer_size = buffer_size
        self.mbps = 0.0
        self.time = 0.0
        self.bytes = 0
        self.direction = direction
        self.stop = False

    def run(self):
        if self.direction == "send":
            data = unhexlify("0"*self.buffer_size)
        while not self.stop:
            if self.direction == "receive":
                t1 = time()
                data = self.sock.recv(self.buffer_size)
                t2 = time()
            else:
                t1 = time()
                self.sock.sendall(data)
                t2 = time()
            self.time += t2-t1
            self.bytes += len(data)
        self.mbps = ((self.bytes * 8) / 1048576)/self.time