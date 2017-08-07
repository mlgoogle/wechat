#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
import config, ProcessLock
import libevent
from multiprocessing import Process, Pipe, Pool
from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager
import jieba



def setConfig():
    eventProcess = Process(target=creatEvent, args=(recCon,))
    eventProcess.start()
    kafkaProcess = Process(target=setkafka(), args=(1,))
    kafkaProcess.start()

def setkafka():
    consumer = KafkaConsumerManager(client=1, host=config.KAFKA_HOST, coname=config.KAFKA_TOPIC)
    consumer.set_callback(callbackMsg)
    consumer.run()

def callbackMsg(msg):
    pool.apply_async(dealwith_event(e=msg, type=1), (msg,))

def writeMsg(msg):
    ProcessLock.lock()
    sendCon.send(msg)
    ProcessLock.unlock()


def initLibEvent():
   return libevent.Base()

def creatEvent(con):
    base = initLibEvent()
    ev = libevent.Event(base, 1, libevent.EV_READ|libevent.EV_PERSIST, recall, con)
    ev.add(0.01)
    base.loop()

def recall(ev, fd, what, event):
    e = event.recv()
    pool.apply_async(dealwith_event(e), (e,))



def dealwith_event(e, type=0):
    if type == 0:
        dealwith_wechatMsg(e)
    elif type == 1:
        dealwith_kafkaMsg(e)

def dealwith_wechatMsg(msg):
    msgText = msg['Text']
    nickName = msg['NickName']
    if msgText.find(config.WIN_RATE_IDENTIFIER) > -1:
        word_list = jieba.lcut(msgText)
        resultList = None
        for text in word_list:
            if text.isdigit():
                resultList.append(text)
    elif msgText.find(config.EVALUTE_IDENTIFIER):
        if endRecordMap[nickName] != True:
            dealwith_endrecord(msg, True)
    else:
        if msgText > 64 & msgText < 69:
            dealwith_endrecord(msg, False)
        elif msgText > 96 & msgText < 101:
            dealwith_endrecord(msg, False)
        pass


def dealwith_endrecord(msg, isdealwith):
    ProcessLock.lock()
    endRecordMap[msg['NickName']] = isdealwith
    ProcessLock.unlock()



def dealwith_kafkaMsg(msg):
    ProcessLock.lock()
    sendMsgToGroup(msg, groupName="ddd")
    ProcessLock.unlock()

    pass

def writerMsgOnKafka(msg):
    ProcessLock.lock()
    producer.push_data(msg)
    ProcessLock.unlock()


# send wechat msg
def sendMsgToGroup(msg, groupName):

    raise NotImplementedError()

def sendMsgToContanct(msg, nickName):

    raise NotImplementedError()

if __name__ == '__main__':
    recCon, sendCon = Pipe(duplex=False)
    pool = Pool(processes=5)
    producer = KafkaProducerManager(client=1, host=config.KAFKA_HOST, coname=config.KAFKA_TOPIC)
    endRecordMap = None