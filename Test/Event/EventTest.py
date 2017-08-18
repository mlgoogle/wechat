import libevent
import socket
import os
from multiprocessing import Process, Pipe
import logging
#import TestChat

logger = logging.getLogger('wechatRobot')

def initLibEvent():
   return libevent.Base()

def creatEvent(con):
    base = initLibEvent()
    ev = libevent.Event(base, con.fileno(), libevent.EV_READ|libevent.EV_PERSIST, recall, con)
    ev.add(0.01)
    base.loop()

def recall(ev, fd, what, event):
    e =  event.recv()
    print e
    if libevent.EV_READ:
	print ev, fd, what, event
