#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process, Pipe
import os
from core import Core
import EventTest

cr = Core()
recCon, sendCon = Pipe(duplex=False)
def wechatLogin(cr):
    cr.auto_login(enableCmdQR=True)
    cr.run()

def initServer(s):
     EventTest.creatEvent(s)


@cr.msg_register('Text')
def receiveMsg(msg):
    if msg['Text'] == 'online':
        sendMsgToGroup('%s : %s' % ( msg['User']['NickName'], msg['Text']))

@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    sendCon.send(msg['Text'])
#    sendMsgToGroup('%s : %s' % ( msg['User']['NickName'], msg['Text']))


def sendMsgToGroup(msg):
    group = cr.search_chatrooms(name='Hero')[0]
    name = group['UserName']
    cr.send(msg, toUserName=name)

#cr.auto_login(enableCmdQR=True)


#cr.run()


recCon, sendCon = Pipe(duplex=False)
p1 = Process(target=wechatLogin, args=(cr,))
p1.start()
p = Process(target=initServer, args=(recCon,))
p.start()
print os.getpid()

