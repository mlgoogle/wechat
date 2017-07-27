import libevent
import os
import threading


def initLibEvent():

   return libevent.Base()

def creatEvent():
    event = threading.Event()
    ev = libevent.Event(initLibEvent(), 'fd', libevent.EV_READ|libevent.EV_PERSIST, recall, event)
    ev.add(1)
    # ev.loop()

def recall(ev, fd, what, event):
    print fd
    print what
    print ev
    print event
    pass


def cycleEvent():
    for index in range(0,10):
        creatEvent()
    