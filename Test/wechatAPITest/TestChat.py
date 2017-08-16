#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process
import jieba
from core import Core

cr = Core()
def wechatLogin(cr):
    cr.auto_login(enableCmdQR=True, hotReload=True)
    cr.run()

@cr.msg_register('Text')
def receiveMsg(msg):
    sendMsgToGroup('dddd')


@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    seg_list = jieba.cut(msg['Text'], cut_all = False)
    sendMsgToGroup('%s : %s' % ('write msg', " ".join(seg_list)))


def sendMsgToGroup(msg):
    cr.get_contact(update=True)
    group = cr.search_friends(remarkName='')
    name = group[0]['UserName']
    cr.send(msg, toUserName=name)


p1 = Process(target=wechatLogin, args=(cr,))
p1.start()



