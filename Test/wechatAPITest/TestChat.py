#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process
from core import Core
cr = Core()

@cr.msg_register('Text')
def receiveMsg(msg):
    sendMsgToGroup(msg['FromUserName'])
    # print msg['FromUserName']
    # cr.send(msg['FromUserName'], toUserName=msg['FromUserName'])
@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    sendMsgToGroup(msg)


def sendMsgToGroup(msg):
    group = cr.search_friends(name='Erwin')[0]
    print group
    print group['UserName']
    name = group['UserName']
    cr.send(msg, toUserName=name)


cr.auto_login(hotReload=True)
cr.run()


