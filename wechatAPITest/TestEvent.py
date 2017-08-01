


from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager

def callbackMsg(msg):
    print msg

producer = KafkaProducerManager(client=1, host='139.224.34.22', coname='robot')
consumer = KafkaConsumerManager(client=1, host='139.224.34.22', coname='robot')
consumer.set_callback(callbackMsg)
producer.push_data('dasd')
producer.push_data('das111d')
consumer.run()

