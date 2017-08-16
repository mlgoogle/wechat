from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager

def callbackMsg(value, key):
    print 'receive msg'
    print value[0], key

consumer = KafkaConsumerManager(client=1, host='122.144.169.214', coname='specialplane_push_robot')
consumer.set_callback(callbackMsg)
consumer.run()
