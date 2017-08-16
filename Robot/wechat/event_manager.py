#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
import config, ProcessLock
import libevent
from multiprocessing import Process, Pipe, Pool
from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager
import jieba
import json

recCon, sendCon = Pipe(duplex=False)
pool = Pool(processes=5)
producer = KafkaProducerManager(client=1, host=config.KAFKA_HOST, coname=config.KAFKA_SEND_TOPIC)
endRecordMap = {'type' : 'endRecord'}
flightRecordMap = {'type' : 'flightRecord'}

#创建事件监听进程
#创建kafka进程
def setConfig():
    eventProcess = Process(target=creatEvent, args=(recCon,))
    eventProcess.start()
#    kafkaProcess = Process(target=setkafka(), args=(1,))
#    kafkaProcess.start()


#设置kafka消费者
def setkafka():
    consumer = KafkaConsumerManager(client=1, host=config.KAFKA_HOST, coname=config.KAFKA_RECEIVE_TOPIC)
    consumer.set_callback(callbackMsg)
    consumer.run()


#kafka消费者回调
def callbackMsg(key,value):
    pool.apply_async(dealwith_event(e=value, type=1, key=key), (value,))


#事件写入
def writeMsg(msg):
    ProcessLock.lock()
    sendCon.send(msg)
    ProcessLock.unlock()


def initLibEvent():
   return libevent.Base()

def creatEvent(con):
    kafkaProcess = Process(target=setkafka(), args=(1,)) 
    kafkaProcess.start()
    base = initLibEvent()
    ev = libevent.Event(base, 1, libevent.EV_READ|libevent.EV_PERSIST, recall, con)
    ev.add(0.01)
    base.loop()

def recall(ev, fd, what, event):
    e = event.recv()
    pool.apply_async(dealwith_event(e), (e,))



def dealwith_event(e, type=0,key = None):
    if type == 0:
        dealwith_wechatMsg(e)
    elif type == 1:
        dealwith_kafkaMsg(e, key=key)

def dealwith_wechatMsg(msg):
    msgText = msg['Text']
    nickName = msg['NickName']
    if msgText.find(config.EVALUTE_IDENTIFIER) > -1:
        word_list = jieba.lcut(msgText)
        resultList = None
        for text in word_list:
            if text.isdigit():
                resultList.append(text)
        if resultList.count > 1:
            rate = resultList[0] / resultList[1]
            if flightRecordMap[nickName]:
                flightInfo = flightRecordMap[nickName]
                parametersMsg = {'flightNum' : flightInfo['flightNum'],
                                 'flightNo' : flightInfo['flightNo'],
                                 'victoryRate' : str(rate)}
            writerMsgOnKafka(json.dumps(parametersMsg), key='pushFlightComplete')
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



def dealwith_kafkaMsg(msg, key):
#    ProcessLock.lock()
    if key == 'pushFlightOrder':
        flightRecordMap[msg['groupName']] = msg
        sendMsgToContanct('亲，您有新的王者专机航班订单，请立刻登机准备起飞！', account=msg['captainAccount'])
    elif key == 'pushFlightStop':
        sendMsgToContanct(('航班停班通知:航班%s停班!', msg['flightNo']), account=msg['captainAccount'])
    else:
        pass
 #   ProcessLock.unlock()


def writerMsgOnKafka(msg,key):
    ProcessLock.lock()
    producer.push_data(msg, key=key)
    ProcessLock.unlock()


# send wechat msg
def sendMsgToGroup(msg, groupName):

    raise NotImplementedError()

def sendMsgToContanct(msg, account):

    raise NotImplementedError()

# if __name__ == '__main__':
