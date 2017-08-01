
from multiprocessing import Process, Pipe
from kafka import kafka_manage_model

def callbackMsg(msg):
    print msg
producer = KafkaProducerManager(host='139.224.34.22', coname = 'robot')
produce.push_data({'test' : 'hha'})

consumer = KafkaConsumerManager(host='139.224.34.22', coname = 'robot')
consumer.set_callback(callbackMsg)


