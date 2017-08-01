


from kafka_manage_model import KafkaConsumerManager
from kafka_manage_model import KafkaProducerManager


def callbackMsg(msg):
    print msg

producer = KafkaProducerManager(client=1, host='139.224.34.22', coname='test')

consumer = KafkaConsumerManager(client=1, host='139.224.34.22', coname='test')
consumer.set_callback(callbackMsg)
consumer.run()
producer.push_data('dasd')
producer.push_data('das111d')

