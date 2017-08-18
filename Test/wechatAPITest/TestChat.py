#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process
from core import Core

cr = Core()

def wechatLogin(core):
    cr.auto_login(enableCmdQR=True, hotReload=True)
    cr.get_contact(update=True)
    cr.run()

@cr.msg_register('Text')
def receiveMsg(msg):
   # event_manager.sendCon.send(msg)
    print msg
    sendMsgToContanct('dd', account='Erwin')
    pass

@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    pass

@cr.msg_register('Friends')
def receiveAddFriend(msg):
    msg.user.verify()
    msg.user.send('欢迎添加机器人 王者小机 !')

def sendMsgToGroup(msg, groupName):
    group = cr.search_chatrooms(name=groupName)[0]
    cr.send(msg, toUserName=group['UserName'])


def sendMsgToContanct(msg, account):
    print account
    print cr.memberList

    contact = cr.search_friends(name=account)[0]
    print contact
    cr.send(msg, toUserName=contact['UserName'])

if __name__ == '__main__':
    wechatLogin(cr)
    # p = Process(target=wechatLogin, args=(cr,))
    # p.start()


