#!/usr/bin/env python
# coding=utf-8

from core import Core

cr = Core()

@cr.msg_register('Text')
def receiveMsg(msg):
    group = cr.search_chatrooms(name='Happy')[0]
    name = group['UserName']
    cr.send('%s : %s' % ( msg['User']['NickName'], msg['Text']), toUserName=name)


@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    group = cr.search_chatrooms(name='Happy')[0]
    name = group['UserName']
    cr.send('%s : %s' % ( msg['User']['NickName'], msg['Text']), toUserName=name)

def sendMsgToGroup(msg):
    group = cr.search_chatrooms(name='Happy')[0]
    name = group['UserName']
    cr.send('%s' % msg, toUserName=name)
cr.auto_login()
sendMsgToGroup('robot has been login.')

cr.run()





