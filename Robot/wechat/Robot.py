#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process
import event_manager
from core import Core

cr = Core()
def wechatLogin(cr):
    cr.auto_login(enableCmdQR=True)
    cr.run()

@cr.msg_register('Text')
def receiveMsg(msg):
    event_manager.sendCon.send(msg)
    pass

@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    event_manager.sendCon.send(msg)
    pass

def sendMsgToGroup(msg, userName):
    # group = cr.search_chatrooms(name='Hero')[0]
    # name = group['UserName']
    # cr.send(msg, toUserName=userName)
    print msg

event_manager.sendMsgToGroup = sendMsgToGroup
event_manager.setConfig()
p1 = Process(target=wechatLogin, args=(cr,))
p1.start()


