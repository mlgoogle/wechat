#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process
from core import Core
from Robot.event import event_manager

cr = Core()
def wechatLogin(cr):
    cr.auto_login(enableCmdQR=True)
    cr.run()

@cr.msg_register('Text')
def receiveMsg(msg):
    if msg['Text'] == 'online':
        sendMsgToGroup('%s : %s' % ( msg['User']['NickName'], msg['Text']))

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


