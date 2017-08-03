
import libevent
from multiprocessing import Process, Pipe, Pool
from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager
from Robot.wechat import config

recCon, sendCon = Pipe(duplex=False)
pool = Pool(processes=5)


def setConfig():
    p = Process(target=creatEvent, args=(recCon,))
    p.start()
    consumer = KafkaConsumerManager(client=1, host=config.KAFKAHOST, coname=config.KAFKATOPIC)
    consumer.set_callback(callbackMsg)
    p1 = Process(target=consumer.run(), args=(1,))
    p1.start()


def callbackMsg(msg):
    pool.apply_async(deal_with_event(), (msg,))

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
    if e.type == 1:
        pool.apply_async(deal_with_event(), (e,))


def deal_with_event(e):
    print e
    pass