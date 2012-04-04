import socket
from binascii import unhexlify
from time import time, clock
from optparse import OptionParser

MSG_OK = unhexlify("01000000")
MSG_NOOK = unhexlify("00000000")
MSG_TCPTEST = unhexlify("01020100dc0500000000000000000000")

def main():
    usage = "usage: %prog [options] HOST"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--port",
                      action="store", dest="port", default=2000)
    parser.add_option("-d", "--duration",
                      action="store", dest="duration", default=8.0,
                      help="test duration in seconds")
    parser.add_option("-m", "--mtu",
                      action="store", dest="mtu", default=1500)

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    HOST = socket.gethostbyname(args[0])
    PORT = int(options.port)
    BUFSIZE = int(options.mtu) - 40
    DURATION = float(options.duration)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    data = s.recv(BUFSIZE)
    if data != MSG_OK:
        print "Cannot connect"
        exit
    
    s.sendall(MSG_TCPTEST)

    data = s.recv(BUFSIZE)
    if data != MSG_OK:
        print "Cannot connect"
        exit

    totaltime = 0.0
    totalbytes = 0
    while totaltime < DURATION:
        t1 = time()
        data = s.recv(BUFSIZE)
        t2 = time()
        totaltime += t2-t1
        totalbytes += len(data)
    s.close()

    totalbits = totalbytes * 8
    print (totalbits/1048576)/totaltime, "Mb/s"

if __name__ == "__main__":
    main()

