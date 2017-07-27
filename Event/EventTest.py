import libevent
import socket

def initLibEvent():

   return libevent.Base()

def creatEvent():

    base = initLibEvent()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind('wechat')
    sock.listen(5)
    connection, adress = sock.accept()
    connection.setblocking(False)

    ev = libevent.Event(base, connection.fileno(), libevent.EV_READ|libevent.EV_PERSIST, recall, connection)
    ev.add(10)
    base.loop()

def recall(ev, fd, what, event):
    print ev, index, what, event
