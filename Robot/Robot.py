#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process

import event_manager
from wechat.core import Core

cr = Core()
def wechatLogin(cr):
    cr.auto_login(enableCmdQR=True)
    cr.run()

@cr.msg_register('Text')
def receiveMsg(msg):
    event_manager.sendCon.send(msg)

@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    event_manager.sendCon.send(msg)
    pass

def sendMsgToGroup(msg):
    group = cr.search_chatrooms(name='Hero')[0]
    name = group['UserName']
    cr.send(msg, toUserName=name)


p1 = Process(target=wechatLogin, args=(cr,))
p1.start()
event_manager.setConfig()


