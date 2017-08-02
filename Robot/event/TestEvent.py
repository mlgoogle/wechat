


from kafka.kafka_manage_model import KafkaConsumerManager
from Event import EventTest
from multiprocessing import Process, Pipe

recCon, sendCon = Pipe(duplex=False)

def initServer(s):
     EventTest.creatEvent(s)



p = Process(target=initServer, args=(recCon,))
p.start()