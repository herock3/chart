
from chartFlaskSocket import HistoryData,PredictData
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
   predictThread =PredictData()
   predictThread.start()

@socketio.on('on_message_history', namespace='/socket')
def message_history():
   print("history.....")
   historyThread = HistoryData()
   historyThread.start()

@socketio.on('on_disconnect', namespace='/socket')
def socket_disconnect():
    print("disconnect")

if __name__ == '__main__':
    socketio.run(app, debug=True)