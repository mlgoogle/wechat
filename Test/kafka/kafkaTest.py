
import json
from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager


produc = KafkaProducerManager(client=1, host='122.144.169.214', coname='robot')
dic = {
    "flightNum": "G2222",
    "flightNo": "G2222-1111",
    "victoryRate": "80"
 }
jsoninfo = json.dumps(dic)
print jsoninfo
produc.push_data(parmas_message= jsoninfo, key='pushFlightComplete')




