
import json
from kafka_manage_model import KafkaConsumerManager, KafkaProducerManager


produc = KafkaProducerManager(client=1, host='122.144.169.214', coname='specialplane_push_robot')
dic = {
    "captainAccount": "Erwin",
    "flightNo": "G2222-1111"
 }
jsoninfo = json.dumps(dic)
print jsoninfo
produc.push_data(parmas_message=jsoninfo, key='pushFlightOrder')




