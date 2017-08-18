# -.- coding:utf-8 -.-
"""
Created on 2016年7月28日

@author: kerry
"""
#from tools.base.mlog import mlog
from collections import Iterable

from kafka import KafkaConsumer,KafkaProducer
import os

class KafkaProducerManager(object):

    def __init__(self, client, host, coname):
        self.client = client
        self.host = host
        self.coname = coname

        self.producer = KafkaProducer(bootstrap_servers=self.host)

    def __del__(self):
        self.producer.close()

    def push_data(self, parmas_message, key=None):
        producer = self.producer
        producer.send(topic=self.coname, parmas_message=parmas_message.encode('utf-8'), key=key)
        producer.flush()



class KafkaConsumerManager(object):
    """
    kafka管理
    """

    def __init__(self, client, host, coname):
        # threading.Thread.__init__(self, name='kafka_manage')
        self.client = client
        self.host = host
        self.coname = coname
        # self.setDaemon(True)
        # self.start()

    def __del__(self):
        pass

    def set_callback(self, callback):
        self.callback = callback



    def run(self):
        """
        连接取数据
        """
       
	while True:
            consumer =  KafkaConsumer(bootstrap_servers=self.host)
            consumer.subscribe([self.coname])
            for message in consumer:
                try:
                    self.callback(key=message[5], value=message[6])
                except Exception, e:
                    print e
 #                   mlog.log().error(e)

