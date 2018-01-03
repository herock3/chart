
import time
import  json
from threading import Lock

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.


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


@socketio.on('on_message_predict', namespace='/socket')
def message_predict():
   print("predicting.....")
   count = 1
   time = 1
   while True:
       socketio.sleep(5)
       count = count + 1
       time = time + 1
       print(count)
       socketio.emit('message_response_predict', {'rul':count, 'cycle':time} ,namespace='/socket')

@socketio.on('on_message_history', namespace='/socket')
def message_predict():
   print("history.....")
   temperature = 1
   while True:
       socketio.sleep(3)
       temperature = temperature + 1
       print('温度:'+str(temperature))
       socketio.emit('message_response_history', {'rul':temperature} ,namespace='/socket')

@socketio.on('on_disconnect', namespace='/socket')
def socket_disconnect():
    print("disconnect")

if __name__ == '__main__':
    socketio.run(app, debug=True)