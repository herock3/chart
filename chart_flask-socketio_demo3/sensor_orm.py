from config.env_config import *
from config.log_config import *
import sqlalchemy
from sqlalchemy import create_engine, inspect, update, delete, Column, Integer, String, Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import time

db_path = DB_NAME +'.db'

Base = declarative_base()
engine = create_engine("sqlite:/// {}".format(str(db_path)))
Session = sessionmaker(bind=engine)
session = Session()

class Sensor(Base):
    __tablename__ = 'Sensor'

    id = Column(Integer, primary_key=True) #primary key
    source = Column(String) # Jabber/Mqtt/Model case sensitive
    sensor_type = Column(String) #LED/Buz/Voice/Air/Temp/Humid
    value = Column(String)
    create_time = Column(String) # Mqtt: Subscribe time Jabber: Http Request Time
    update_time = Column(String) # Mqtt: DB save time   Jabber: Publish Time

Base.metadata.create_all(engine)

def GetLastRecordsByType(st):

    # Get last not update record from DB
    try:
        _sensor = session.query(Sensor).filter(Sensor.update_time != None).filter(Sensor.sensor_type == st).order_by(Sensor.id.desc()).first()
        return _sensor
    except Exception as e:
        session.rollback()
        raise(e)
    finally:
        session.close()

def Insert_Records(src, st, val, ct, ut):
    # insert data to sensor table
    try:
        _data = Sensor(source=src,sensor_type=st,value=val,create_time=ct,update_time=ut)
        session.add(_data)
        session.flush()
        _id = _data.id
        session.commit()
        return _id
    except Exception as e:
        session.rollback()
        raise(e)
    finally:
        session.close()

def UpdateTimebyId(id, current_time):

    try:
        _update = update(Sensor).where(Sensor.id == id).values(update_time= current_time)
        session.execute(_update)
        session.commit()

    except Exception as e:
        session.rollback()
        raise(e)
    finally:
        session.close()

def DeleteById(id):

    try:
        _delete = delete(Sensor).where(Sensor.id == id)
        # _delete = delete(Sensor).where(Sensor.source == 'Test')
        session.execute(_delete)
        session.commit()

    except Exception as e:
        session.rollback()
        raise(e)
    finally:
        session.close()

