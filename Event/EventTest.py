import libevent
import os
import threading


def initLibEvent(self):

   return libevent.Base()

def creatEvent():
    event = threading.Event()
    ev = libevent.Event(initLibEvent(), 'fd', libevent.EV_READ|libevent.EV_PERSIST, recall, event)

def recall(ev, fd, what, event):
    print fd
    print what
    print ev
    print event
    pass


