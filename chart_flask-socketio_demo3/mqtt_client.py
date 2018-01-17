from config.env_config import *
from config.log_config import *
from sensor_orm import *
from multiprocessing import Queue
import paho.mqtt.client as mqtt
import threading
import time
import json

class MqttClient(threading.Thread):

    '''mqtt mqtt_client to consume message.'''
    def __init__(self):
        threading.Thread.__init__(self)
        self.mqtt_client = mqtt.Client()
        self.mqtt_broker = os.environ.get('MQTT_BROKER', MQTT_BROKER)
        self.mqtt_port = int(os.environ.get('MQTT_PORT', MQTT_PORT))
        self.mqtt_input_topic1 = "ddp/temp"
        self.mqtt_input_topic2 = 'ddp/air'
        self.mqtt_input_topic3 = 'ddp/voice'
        self.mqtt_input_topic4 = 'ddp/hum'
        self.mqtt_input_topic5 = 'ddp/iot'
        self.sensor_queue = Queue(maxsize = 100)
        self.model_queue = Queue(maxsize = 100)
        self.jabbot_queue = Queue(maxsize = 100)

        LOG.info('mqtt broker:{}, port:{} '.format(self.mqtt_broker, self.mqtt_port))

    #to update status
    def stop_mqttclient(self):
        LOG.info('stop mqtt client for broker: {} '.format(self.mqtt_broker))
        try:
            self.mqtt_client.disconnect()
            print("mqttclient disconnect")
        except:
            pass
     
    #call back func.
    def on_message(self,client,userdata, message):
        try:
            _msg = json.loads(str(message.payload, encoding = "utf-8"))
            _data = {}
            _data['Type'] = message.topic
            _data['Msg'] = _msg

            if message.topic == self.mqtt_input_topic5:
                _data['Msg'] = _data['Msg']['real']
                self.model_queue.put(json.dumps(_data))
                LOG.info("dumps {}".format(_data))
                # _id = Insert_Records('Model', _data['Type'], _data['Msg'], time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()), None)
            else:
                self.sensor_queue.put(json.dumps(_data))
                LOG.info("dumps {}".format(_data))
                # _id = Insert_Records('Mqtt', _data['Type'], str(_data['Msg']), time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()), None)

            LOG.info('*** mqtt client for topic {} received message: {} . Message Id: {}.'.format(message.topic,_msg, _id))
            
        except Exception as ex:
            LOG.error(str(ex))

	#on connect.
    def on_connect(self, client, userdata, flags, rc):
        # LOG.info("connecting to server to subscribe at {} ...".format(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())))
        print("connecting to server to subscribe at {} ...".format(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())))
        self.mqtt_client.subscribe(self.mqtt_input_topic1)
        self.mqtt_client.subscribe(self.mqtt_input_topic2)
        self.mqtt_client.subscribe(self.mqtt_input_topic3)
        self.mqtt_client.subscribe(self.mqtt_input_topic4)
        self.mqtt_client.subscribe(self.mqtt_input_topic5)
        
    #thread.

    def run(self):
        try:
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, MQTT_KEEPLIVE)
            self.mqtt_client.enable_logger(LOG)
            self.mqtt_client.loop_forever()
        except Exception as ex:
            LOG.error(str(ex))
        finally:
            self.mqtt_client.disconnect()