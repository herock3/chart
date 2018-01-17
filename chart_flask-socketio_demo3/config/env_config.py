#service port.
SERVICE_PORT = 5152
#DEBUG
IS_DEBUG = False

#db path.
# DB_PATH = 'data/db'
#db config
DB_NAME = 'yunchen'
#sensor data.
# SENSOR_TABLE_NAME = 'sensor_details'
#sensor table column list.
SENSOR_COLUMNS = ['id', 'type','value','time']

#predict data
PREDICT_TABLE_NAME = 'predict_data'
#take top n records do predict
TOP_NUM = 6

##mqtt config###########
# MQTT_BROKER = '10.75.161.193'
MQTT_BROKER = '54.179.158.64'
MQTT_PORT = 1883
MQTT_TOPIC = 'mqtt-topic'
#mqtt connection keeplive
MQTT_KEEPLIVE = 60



