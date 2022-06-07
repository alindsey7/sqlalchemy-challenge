#imports
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#creating engine
engine = create_engine('sqlite:///hawaii.sqlite')

#Reflecting DB
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def index():
    return(
        f'Available Routes in Climate API: <br>'
        f'/api/v1.0/precipitation<br>'
        f'/api/v1.0/stations<br>'
        f'/api/v1.0/tobs<br>'
        f'/api/v1.0/start<br>'
        f'/api/v1.0/start/end'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session= Session(engine)
    rain = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23')
    session.close()

    rain_last_year = []
    for date, prcp in rain:
        rain_dict = {}
        rain_dict['Date'] = date
        rain_dict['Prcp'] = prcp
        rain_last_year.append(rain_dict)
    return jsonify(rain_last_year)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    all_stations = session.query(Station.station).all()
    session.close()

    stations_list = list(np.ravel(all_stations))

    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def temp():
    session = Session(engine)
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()
    session.close()

    temps_list = list(np.ravel(temps))

    return jsonify(temps_list)

@app.route('/api/v1.0/<start>')
def start(start):
    session=Session(engine)
    temps = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    temps_list = list(np.ravel(temps))

    return jsonify(temps_list)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    session=Session(engine)
    temps = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temps_list = list(np.ravel(temps))

    return jsonify(temps_list)

if __name__ == '__main__':
    app.run(debug=True)