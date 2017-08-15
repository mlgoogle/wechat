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
   # event_manager.sendCon.send(msg)
    pass

@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    event_manager.sendCon.send(msg.deepcopy())
    pass

@cr.msg_register('Friends')
def receiveAddFriend(msg):
    cr.add_friend(**msg['Text'])
    cr.get_contract()
    cr.send_msg('欢迎添加机器人 王者小机 !', msg['RecommendInfo']['UserName'])

def sendMsgToGroup(msg, groupName):
    group = cr.search_chatrooms(name=groupName)[0]
    cr.send(msg, toUserName=group['UserName'])

def sendMsgToContanct(msg, account):
    contact = cr.search_friends(wechatAccount=account)
    cr.send(msg, toUserName=contact['UserName'])

if __name__ == '__main__':
    event_manager.sendMsgToGroup = sendMsgToGroup
    event_manager.sendMsgToContanct = sendMsgToContanct
    event_manager.setConfig()
    wechatLogin(cr)
    # p = Process(target=wechatLogin, args=(cr,))
    # p.start()


