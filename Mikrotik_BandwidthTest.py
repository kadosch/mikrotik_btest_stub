from optparse import OptionParser
from TcpTest import TcpTest
from time import sleep
import socket
import messages
import hashlib

def md5(content):
    m = hashlib.md5()
    m.update(content)
    return m.digest()

def main():
    usage = "usage: %prog [options] HOST"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--port",
        action="store", dest="port", default=2000)
    parser.add_option("-t", "--time",
        action="store", dest="duration", default=8.0,
        help="test duration in seconds")
    parser.add_option("-m", "--mtu",
        action="store", dest="mtu", default=1500)
    parser.add_option("-d", "--direction",
        action="store", dest="direction", default="receive",
        help="test direction: receive, send, both")
    parser.add_option("-u", "--user",
        action="store", dest="user", default="")
    parser.add_option("-a", "--password",
        action="store", dest="password", default="")

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    host = socket.gethostbyname(args[0])
    port = int(options.port)
    bufsize = int(options.mtu) - 40
    duration = float(options.duration)
    direction = options.direction
    user = options.user[:32]
    password = options.password
    if direction in ("receive", "send"):
        directions = [direction]
    elif direction == "both":
        directions = ["receive", "send"]
    else:
        exit(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    if s.recv(bufsize) != messages.OK:
        s.close()
        exit(1)

    if direction == "receive":
        s.sendall(messages.TCP_DOWN)
    elif direction == "send":
        s.sendall(messages.TCP_UP)
    else:
        s.sendall(messages.TCP_BOTH)

    data = s.recv(bufsize)

    if data != messages.OK:
        if len(data) != 20 or data[:4] != '\x02\x00\x00\x00':
            s.close()
            exit()
        challenge = data[4:]
        response = md5(password+md5(password+challenge)) + user + ('\x00' * (32-len(user)))
        s.sendall(response)
        data2 = s.recv(bufsize)
        if  data2 != messages.OK:
            s.close()
            exit(1)

    thread_list = list()
    for d in directions:
        th = TcpTest(s, bufsize, d)
        thread_list.append(th)
        th.start()

    sleep(duration)

    for th in thread_list:
        th.stop = True

    for th in thread_list:
        th.join()
        if th.direction == "receive":
            print "Rx: ", round(th.mbps, 2),"Mb/s"
        else:
            print "Tx: ", round(th.mbps, 2),"Mb/s"
    s.close()


if __name__ == "__main__":
    main()
