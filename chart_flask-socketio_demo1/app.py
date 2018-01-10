
import math
from threading import Lock

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


thread = None
thread_lock = Lock()


@app.route('/')
def index_page():
    return render_template('index.html')

@socketio.on('on_connect', namespace='/socket')
def socket_connect():
   print("connecting.....")
   temperature = 0
   humidity=0
   sound=0
   pm=0
   count = 0
   time = 0
   while True:
       socketio.sleep(6)
       temperature = temperature + 1
       humidity = humidity + 1
       sound = sound + 1
       pm = pm + 1
       count = math.sin(pm)
       time = time + 1
       print('温度:' + str(temperature))
       socketio.emit('message_response_history', {'temperature': temperature,'humidity': humidity,'sound':sound,'pm':pm}, namespace='/socket')
       socketio.emit('message_response_predict', {'rul':count, 'cycle':time} ,namespace='/socket')

@socketio.on('on_message_predict', namespace='/socket')
def message_predict():
   print("predicting.....")

@socketio.on('on_message_history', namespace='/socket')
def message_history():
   print("history.....")


@socketio.on('on_disconnect', namespace='/socket')
def socket_disconnect():
    print("disconnect")

if __name__ == '__main__':
    socketio.run(app, debug=True)