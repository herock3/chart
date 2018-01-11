import threading

import socketio


class HistoryData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        temperature = 0
        humidity = 0
        sound = 0
        pm = 0
        while True:
            socketio.sleep(3)
            temperature = temperature + 1
            humidity = humidity + 1
            sound = sound + 1
            pm = pm + 1
            print('温度:' + str(temperature))
            socketio.emit('message_response_history',
                          {'temperature': temperature, 'humidity': humidity, 'sound': sound, 'pm': pm},
                          namespace='/socket')