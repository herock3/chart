from config.env_config import *
from config.log_config import *

from sensor_orm import *
from mqtt_client import *
from mqtt_producer import *
import json
import tornado
import tornado.web
import random
import time
from tornado.websocket import WebSocketHandler

global mqttc
# global mqttc_dict
# global chatbot_flag
mqttc = MqttClient()
mqttc.start()
# mqttc_dict[1] = mqttc

def Web2Mqtt(_type, _response):
    global mqttp
    global mqttc
    _id = Insert_Records('Test',_response['Type'],_response['value'],time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),None)
    mqttp = MqttProducer(_id)
    mqttp.start()
    mqttp.chatbot_queue.put(json.dumps(_response))
    mqttc.jabbot_queue.put(json.dumps(_response))

    return _id

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

    # Cross Origin
    def check_origin(self,origin):
        return True

# Get Rest Api request from Jabber and put into Mqtt Queue to publish
class LED_Handler(tornado.web.RequestHandler):

    def get(self, id):
        
        _response = {'Type':'LED','value':int(id)}
        _id = Web2Mqtt('LED',_response)
        self.write("Called sensor LED with message id {}".format(_id))

class Buz_Handler(tornado.web.RequestHandler):

    def get(self,id):
        _response = {'Type':'Buz','value':int(id)}
        _id = Web2Mqtt('Buz',_response)
        self.write("Called sensor Buz with message id {}".format(_id))
        
# Get Rest Api requst from Model and call
class Strategy_Handler(tornado.web.RequestHandler):

    def get(self, id):
        self.write("Called sensor LED with message id {}".format(int(id)))
        

class Live_Handler(tornado.web.RequestHandler):
    
    def get(self, id):
        global mqttc
        self.write("Switched to live video {}".format(int(id)))
        _response = {'Type':'Video','value':int(id)}
        mqttc.jabbot_queue.put(json.dumps(_response))
        print(" dumps {}".format(_response))
        

class ModelOutputs_Handler(tornado.web.RequestHandler):
    def get(self):
        self.write("No data received")

    def post(self):
        data = self.get_argument("input_map")


# Websockets
class Socket_Sender(WebSocketHandler):

    def open(self):
        pass

    def on_message(self, message):
   
        global mqttc, mq, st, jab
              
        if (mqttc.model_queue.qsize() > 0) or (mqttc.sensor_queue.qsize() > 0) or (mqttc.jabbot_queue.qsize() > 0):
            mq = SocketSender(self,mqttc.model_queue,'model')
            st = SocketSender(self,mqttc.sensor_queue,'sensor')
            jab = SocketSender(self,mqttc.jabbot_queue,'jabber')
            st.start()
            mq.start()
            jab.start()


    def on_close(self):
        global mqttc, mq, st, jab
        print("Websocket closed")
        mqttc.stop_mqttclient()
        st.join()
        mq.join()
        jab.join()
    
    def send_jabbot(self):
        _led = {"Type":"jabber","message":{'Type': 'LED', 'value': 0}}
        _buz = {"Type":"jabber","message":{'Type': 'Buz', 'value': 1}}
        self.write_message(_led)
        self.write_message(_buz)


class SocketSender(threading.Thread):
    def __init__(self, socker_sender, queue, is_type):
        threading.Thread.__init__(self)
        self.socker_sender = socker_sender
        self.queue = queue
        self.is_type = is_type

    def run(self):
        global mqttc_dict

        while True:
                LOG.debug('===socket sender thread running, is type:{} ....'.format(self.is_type))
                _msg = self.queue.get()
                #send msg.
                if self.is_type == 'model':
                    msg = {"Type":"model","message":_msg}
                    self.socker_sender.write_message(msg)
                    time.sleep(0)
                elif self.is_type == 'sensor':
                    msg = {"Type":"sensor","message":_msg}
                    self.socker_sender.write_message(msg)
                    time.sleep(0)
                elif self.is_type == 'jabber':
                    msg = {"Type":"jabber","message":_msg}
                    self.socker_sender.write_message(msg)
                    print("Socket sending message {}".format(msg))
                    time.sleep(0)
                else:
                    return True
