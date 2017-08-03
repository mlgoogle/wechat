
import config
# from . import config

import libevent
from multiprocessing import Process, Pipe, Pool
from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager


recCon, sendCon = Pipe(duplex=False)
pool = Pool(processes=5)


def setConfig():
    p = Process(target=creatEvent, args=(recCon,))
    p.start()
    p1 = Process(target=setkafka(), args=(1,))
    p1.start()
def setkafka():
    consumer = KafkaConsumerManager(client=1, host=config.KAFKAHOST, coname=config.KAFKATOPIC)
    consumer.set_callback(callbackMsg)
    consumer.run()
def callbackMsg(msg):
    pool.apply_async(deal_with_event(e=msg, type=1), (msg,))

def writeMsg(msg):
    sendCon.send(msg)
    pass


def initLibEvent():
   return libevent.Base()

def creatEvent(con):
    base = initLibEvent()
    ev = libevent.Event(base, 1, libevent.EV_READ|libevent.EV_PERSIST, recall, con)
    ev.add(0.01)
    base.loop()

def recall(ev, fd, what, event):
    e = event.recv()
    pool.apply_async(deal_with_event(e), (e,))



def deal_with_event(e, type=0):
    if type == 0:
        dealwith_wechatMsg(e)
    elif type == 1:
        dealwith_kafkaMsg(e)

def dealwith_wechatMsg(msg):
    sendMsgToGroup(msg, userName='111')
    pass

def dealwith_kafkaMsg(msg):
    sendMsgToGroup(msg, userName='111')
    pass

def sendMsgToGroup(msg, userName):

    raise NotImplementedError()
