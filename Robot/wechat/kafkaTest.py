

from kafka.kafka_manage_model import KafkaConsumerManager


def callbackMsg(msg):
    print msg

consumer = KafkaConsumerManager(client=1, host='139.224.34.22', coname='robot')
consumer.set_callback(callbackMsg)
consumer.run()

