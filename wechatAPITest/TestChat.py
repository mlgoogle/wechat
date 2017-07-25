#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8

from core import Core

cr = Core()

@cr.msg_register('Text')
def receiveMsg(msg):
    if msg['Text'] == 'online':
        sendMsgToGroup('%s : %s' % ( msg['User']['NickName'], msg['Text']))

@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    if msg['User']['NickName'] == 'Hero':
        sendMsgToGroup('%s : %s' % ( msg['User']['NickName'], msg['Text']))


def sendMsgToGroup(msg):
    group = cr.search_chatrooms(name='Hero')[0]
    name = group['UserName']
    cr.send('%s' % msg, toUserName=name)


cr.auto_login(enableCmdQR=True)

# sendMsgToGroup('robot has been login.')
cr.run()





