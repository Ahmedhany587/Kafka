from kafka import KafkaProducer
from data import get_Weather_data
import json
import time



def json_serializer(data):
    return json.dumps(data).encode("utf-8")

producer = KafkaProducer(bootstrap_servers= ['localhost:9092'],value_serializer=json_serializer)

if __name__ == "__main__":
    while 1 == 1:
        data = get_Weather_data()
        print(data)
        producer.send("KafkaProject",data)
        time.sleep(1)
        
