from sensor_orm import *
from mqtt_client import *

class SocketSender:
    '''send socket message.'''
    def __init__(self, socketio, input_type, queue):
        # threading.Thread.__init__(self)
        self.input_type = input_type
        self.queue = queue
    #thread.
    def run(self):
        LOG.info('****socket sender thread start, is predict:{}'.format(self.is_predict))
        global mqttc_dict
        try:
            while True:
                if not len(mqttc_dict):
                    break
                LOG.debug('===socket sender thread running, is predict:{} ....'.format(self.is_predict))
                #get msg.
                msg = self.queue.get()
                #send msg.
                if self.is_predict:
                    self.write_message('message_response_model', json.dumps(dict(status=200, result=msg))) 
                else:
                    self.write_message('message_response_sensor', json.dumps(dict(status=200, result=msg)))
                LOG.debug('...sending response message:{}'.format(json.dumps(dict(status=200, result=msg))))
        except Exception as ex:
            LOG.error('error happens in socket sender: {}'.format(str(ex)))   

