#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
from multiprocessing import Process
import libevent
from RobotEvent import RobotEvent
import event_manager
from core import Core
from multiprocessing import Pipe
cr = Core()
print cr
recCon, sendCon = Pipe(duplex=False)

def wechatLogin(core):
    cr.auto_login(enableCmdQR=True, hotReload=True)
    cr.run()

def writeMsg(sendCon,msg, account):
    print msg, account
    e = RobotEvent(account=account, msg=msg)
    sendCon.send(e)

def initLibEvent():
   return libevent.Base()

def creatEvent(con):
    base = initLibEvent()
    ev = libevent.Event(base, 1, libevent.EV_READ|libevent.EV_PERSIST, recall, con)
    ev.add(0.01)
    base.loop()

def recall(ev, fd, what, event):
    print ev
    e = event.recv()
    print e
    if e:
        sendMsgToContanct(e.msg, account=e.account)

@cr.msg_register('Text')
def receiveMsg(msg):
   # event_manager.sendCon.send(msg)
    pass

@cr.msg_register('Text', isGroupChat=True)
def receiveGrope(msg):
    event_manager.sendCon.send(msg)
    pass

@cr.msg_register('Friends')
def receiveAddFriend(msg):
    msg.user.verify()
    msg.user.send('欢迎添加机器人 王者小机 !')

def sendMsgToGroup(msg, groupName):

    group = cr.search_chatrooms(name=groupName)[0]
    cr.send(msg, toUserName=group['UserName'])


def sendMsgToContanct(msg, account):
    print msg
    contact = cr.search_friends(name=account)[0]
    cr.send(msg, toUserName=contact['UserName'])


if __name__ == '__main__':
    event_manager.setConfig(robotCon=sendCon)
    p = Process(target=creatEvent, args=(recCon,))
    p.start()
    wechatLogin(cr)



