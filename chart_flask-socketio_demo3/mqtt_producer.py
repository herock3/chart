#! /usr/bin/env python
from config.env_config import *
from config.log_config import *
from sensor_orm import *
from multiprocessing import Queue
import paho.mqtt.client as mqtt
import threading
import time

class MqttProducer(threading.Thread):
    '''mqtt mqtt_client to publish message.'''
    def __init__(self, msg_id):
        threading.Thread.__init__(self)
        self.mqtt_client = mqtt.Client()
        self.mqtt_broker = os.environ.get('MQTT_BROKER', MQTT_BROKER)
        self.mqtt_port = int(os.environ.get('MQTT_PORT', MQTT_PORT))
        self.mqtt_topic = 'ddp/sensor'
        self.chatbot_queue = Queue(maxsize = 100)
        self.msg_id = msg_id
        # LOG.info('mqtt broker:{}, port:{}, topic:{}'.format(self.mqtt_broker, self.mqtt_port, self.mqtt_topic))

    #to update status
    def stop_mqttclient(self):
        LOG.info('stop mqtt client for broker: {}, topic:{}'.format(self.mqtt_broker, self.mqtt_topic))
        try:
            self.mqtt_client.disconnect()
        except:
            pass

    def on_publish(self, client, userdata, mid):
        try:

            UpdateTimebyId(self.msg_id, time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()))
            LOG.info("publish time {}".format(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())))
            #save to db. update publish time
            #LOG.debug('*** mqtt client publish message id: {} '.format(mid))
        except Exception as e:
            raise(e)

	#on connect.
    def on_connect(self, client, userdata, flags, rc):
        # get publish data from db
        LOG.info("connecting to server to publish at {} ...".format(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime())))
        
        while not self.chatbot_queue.empty():
            _msg = self.chatbot_queue.get()
            LOG.info("sending message {} ...".format(_msg))
            self.mqtt_client.publish(self.mqtt_topic,_msg)

    #thread.
    def run(self):
        try:
            self.mqtt_client.on_connect = self.on_connect
            self.mqtt_client.on_publish = self.on_publish
            self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, MQTT_KEEPLIVE)
            self.mqtt_client.enable_logger(LOG)
            self.mqtt_client.loop_forever()
        except Exception as ex:
            # LOG.error(str(ex))
            print(str(ex))
        finally:
            self.mqtt_client.disconnect()