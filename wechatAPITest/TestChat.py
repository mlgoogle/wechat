#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process, Pipe
import os
from core import Core
import EventTest
import jieba
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
    seg_list = jieba.cut(msg['Text'], cut_all = False)
    sendMsgToGroup('%s : %s' % ('write msg', " ".join(seg_list)))


def sendMsgToGroup(msg):
    group = cr.search_chatrooms(name='Hero')[0]
    name = group['UserName']
    cr.send(msg, toUserName=name)


p = Process(target=initServer, args=(recCon,))
p.start()
p1 = Process(target=wechatLogin, args=(cr,))
p1.start()


