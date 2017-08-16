#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process
import jieba
from core import Core
cr = Core()

@cr.msg_register('Text')
def receiveMsg(msg):
    sendMsgToGroup(msg)


@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    seg_list = jieba.cut(msg['Text'], cut_all = False)
    sendMsgToGroup('%s : %s' % ('write msg', " ".join(seg_list)))


def sendMsgToGroup(msg):
    group = cr.search_friends()
    name = group[0]['UserName']
    cr.send(msg, toUserName=name)


cr.auto_login(enableCmdQR=2)
cr.run()


