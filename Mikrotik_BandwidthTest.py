from optparse import OptionParser
from TcpTest import TcpTest
from time import sleep
import socket
import messages

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

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    host = socket.gethostbyname(args[0])
    port = int(options.port)
    bufsize = int(options.mtu) - 40
    duration = float(options.duration)
    direction = options.direction
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

    if s.recv(bufsize) != messages.OK:
        s.close()
        exit()

    thread_list = list()
    for d in directions:
        th = TcpTest(s, bufsize, d)
        thread_list.append(th)
        th.start()

    sleep(duration)

    for th in thread_list:
        th.stop = True

    rx_mbps = 0.0
    tx_mbps = 0.0
    for th in thread_list:
        th.join()
        if th.direction == "receive":
            rx_mbps += th.mbps
        else:
            tx_mbps += th.mbps
    s.close()

    if direction in ("receive","both"):
        print "Rx: ", round(rx_mbps, 2),"Mb/s"
    if direction in ("send", "both"):
        print "Tx: ", round(tx_mbps, 2),"Mb/s"

if __name__ == "__main__":
    main()
