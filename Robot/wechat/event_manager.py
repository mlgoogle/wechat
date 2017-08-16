#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8
import config, ProcessLock
import libevent
from multiprocessing import Process, Pipe, Pool
from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager
import jieba
import json
from RobotEvent import RobotEvent

class event_manager(object):
    def __init__(self, robotCon):
        self.robotCon = robotCon
        print robotCon
        self.producer = KafkaProducerManager(client=1, host=config.KAFKA_HOST, coname=config.KAFKA_SEND_TOPIC)
        self.pool = Pool(processes=5)
        self.endRecordMap = {'type' : 'endRecord'}
        self.flightRecordMap = {'type' : 'flightRecord'}


    def setConfig(self):
        eventProcess = Process(target=self.creatEvent, args=(self.robotCon,))
        eventProcess.start()

    def initLibEvent(self):
        return libevent.Base()

    def setkafka(self):
        consumer = KafkaConsumerManager(client=1, host=config.KAFKA_HOST, coname=config.KAFKA_RECEIVE_TOPIC)
        consumer.set_callback(self.callbackMsg)
        consumer.run()

    def callbackMsg(self,key, value):
        self.pool.apply_async(self.dealwith_event(e=json.loads(value), type=1, key=key), (value,))

    def creatEvent(self, con):
        kafkaProcess = Process(target=self.setkafka(), args=(1,))
        kafkaProcess.start()
        base = self.initLibEvent()
        ev = libevent.Event(base, 1, libevent.EV_READ | libevent.EV_PERSIST, self.recall, con)
        ev.add(0.01)
        base.loop()

    def recall(self, ev, fd, what, event):
        e = event.recv()
        print e
        self.pool.apply_async(self.dealwith_event(e), (e,))

    def dealwith_event(self, e, type=0, key=None):
        if type == 0:
            self.dealwith_wechatMsg(e)
        elif type == 1:
            self.dealwith_kafkaMsg(e, key=key)

    def dealwith_wechatMsg(self, msg):
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
                print 'find flight end', nickName
                if self.flightRecordMap[nickName]:
                    flightInfo = self.flightRecordMap[nickName]
                    parametersMsg = {'flightNum': flightInfo['flightNum'],
                                     'flightNo': flightInfo['flightNo'],
                                     'victoryRate': str(rate)}
                    self.writerMsgOnKafka(json.dumps(parametersMsg), key='pushFlightComplete')
        elif msgText.find(config.EVALUTE_IDENTIFIER):
            if self.endRecordMap[nickName] != True:
                self.dealwith_endrecord(msg, True)
        else:
            if msgText > 64 & msgText < 69:
                self.dealwith_endrecord(msg, False)
            elif msgText > 96 & msgText < 101:
                self.dealwith_endrecord(msg, False)
            pass

    def dealwith_endrecord(self, msg, isdealwith):
        self.endRecordMap[msg['NickName']] = isdealwith

    def dealwith_kafkaMsg(self, msg, key):
        if key == 'pushFlightOrder':
            self.flightRecordMap[msg['groupName']] = msg
            mes = '您的航班【 %s 】已售出票，请到微信群【%s】，联系相关乘客，做好登机前准备。' % (msg['flightNo'], msg['groupName'])
            account = msg['captainAccount']
            e = {'msg': mes,
                 'account' : account
            }
            self.robotCon.send(e)
        elif key == 'pushFlightStop':
            mes = '您的航班【 %s 】已停班。' % (msg['flightNo'])
            account = msg['captainAccount']
            e = {'msg':mes,
                'account':account
            }
            self.robotCon.send(e)
            pass
        else:
            pass

    def writerMsgOnKafka(self, msg, key):
        self.producer.push_data(msg, key=key)

# send, rec = Pipe()
# RobotCon = send
# print RobotCon
# pool = Pool(processes=5)
# producer = KafkaProducerManager(client=1, host=config.KAFKA_HOST, coname=config.KAFKA_SEND_TOPIC)
# endRecordMap = {'type' : 'endRecord'}
# flightRecordMap = {'type' : 'flightRecord'}
#
# #创建事件监听进程
# #创建kafka进程
# def setConfig(robotCon):
#     RobotCon = robotCon
#     print robotCon
#     eventProcess = Process(target=creatEvent, args=(robotCon,))
#     eventProcess.start()
#
#
#
# #设置kafka消费者
# def setkafka():
#     consumer = KafkaConsumerManager(client=1, host=config.KAFKA_HOST, coname=config.KAFKA_RECEIVE_TOPIC)
#     consumer.set_callback(callbackMsg)
#     consumer.run()
#
#
# #kafka消费者回调
# def callbackMsg(key,value):
#     pool.apply_async(dealwith_event(e=json.loads(value), type=1, key=key), (value,))



#
# def initLibEvent():
#    return libevent.Base()
#
# def creatEvent(con):
#     kafkaProcess = Process(target=setkafka(), args=(1,))
#     kafkaProcess.start()
#     base = initLibEvent()
#     ev = libevent.Event(base, 1, libevent.EV_READ|libevent.EV_PERSIST, recall, con)
#     ev.add(0.01)
#     base.loop()
#
# def recall(ev, fd, what, event):
#     e = event.recv()
#     pool.apply_async(dealwith_event(e), (e,))
#
#
#
# def dealwith_event(e, type=0,key = None):
#     if type == 0:
#         dealwith_wechatMsg(e)
#     elif type == 1:
#         dealwith_kafkaMsg(e, key=key)
#
# def dealwith_wechatMsg(msg):
#     msgText = msg['Text']
#     nickName = msg['NickName']
#     if msgText.find(config.EVALUTE_IDENTIFIER) > -1:
#         word_list = jieba.lcut(msgText)
#         resultList = None
#         for text in word_list:
#             if text.isdigit():
#                 resultList.append(text)
#         if resultList.count > 1:
#             rate = resultList[0] / resultList[1]
#             if flightRecordMap[nickName]:
#                 flightInfo = flightRecordMap[nickName]
#                 parametersMsg = {'flightNum' : flightInfo['flightNum'],
#                                  'flightNo' : flightInfo['flightNo'],
#                                  'victoryRate' : str(rate)}
#             writerMsgOnKafka(json.dumps(parametersMsg), key='pushFlightComplete')
#     elif msgText.find(config.EVALUTE_IDENTIFIER):
#         if endRecordMap[nickName] != True:
#             dealwith_endrecord(msg, True)
#     else:
#         if msgText > 64 & msgText < 69:
#             dealwith_endrecord(msg, False)
#         elif msgText > 96 & msgText < 101:
#             dealwith_endrecord(msg, False)
#         pass
#
#
# def dealwith_endrecord(msg, isdealwith):
#     endRecordMap[msg['NickName']] = isdealwith
#
#
#
# def dealwith_kafkaMsg(msg, key):
#     if key == 'pushFlightOrder':
#         flightRecordMap[msg['groupName']] = msg
#         mes = '亲，您有新的王者专机航班订单，请立刻登机准备起飞！'
#         account = msg['captainAccount']
#         e = RobotEvent(account=account, msg=mes)
#         print account
#         print RobotCon
#         RobotCon.send(e)
#     elif key == 'pushFlightStop':
#         pass
#       #  Robot.writeMsg(sendCon=RobotCon, msg=('航班停班通知:航班%s停班!', msg['flightNo']), account=msg['captainAccount'])
#     else:
#         pass
#
#
# def writerMsgOnKafka(msg,key):
#     producer.push_data(msg, key=key)


# if __name__ == '__main__':
