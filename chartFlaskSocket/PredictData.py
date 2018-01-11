import threading

import socketio


class PredictData(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        count = 0
        time = 0
        while True:
            socketio.sleep(3)
            count = count + 1
            time = time + 1
            socketio.emit('message_response_predict', {'rul': count, 'cycle': time}, namespace='/socket')