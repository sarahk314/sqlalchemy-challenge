# Import dependencies

import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct
from flask import Flask, jsonify 

# Set up database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Set up Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    
    """List all available api routes."""
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start format:YYYY-MM-DD]<br/>"
        f"/api/v1.0/[start format:YYYY-MM-DD]/[end format:YYYY-MM-DD]<br/>"

        
@app.route("/api/v1.0/precipitation")
def precipitation():
        
        session = Session(engine)
        
        """List all daily precipitation totals for the past 12 months."""
        
        last_date = '2017-08-23'
        start_date = '2016-08-23'
        
        results = session.query(Measurement.prcp, Measurement.date).\
            filter(Measurement.date >= one_yr_ago).\
            filter(Measurement.date <= date).\
            order_by(Measurement.date).all()
        
        session.close()
        
        prcp_values = []
        for prcp, date in results:
            prcp_dict = {}
            prcp_dict["precipitation"] = prcp
            prcpdict["date"] = date
            prcp_values.append(precipitation_dict)
        return jsonify(prcp_values)

        
@app.route("/api/v1.0/stations")
def station(): 
    
        session = Session(engine)
        
        """List all active weather stations."""
        
        results = session.query(Station.station).order_by(Station.station).all()
        
        session.close()
        
        stations = list(np.ravel(results))
        return jsonify(stations)

        
@app.route("/api/v1.0/tobs") 
def tobs():
        
        session = Session(engine)
        
        """List data observed for the most active station from the past 12 months."""
        
        start_date = '2016-08-18'
        
        results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == most_active).\
            filter(Measurement.date > '2016-08-18').\
            order_by(Measurement.date).all()
        
        session.close()
        
        dates = []
        observations = []
        
        for date, observation in results:
            dates.append(date)
            observations.append(observation)
        
        most_active_dict = dict(zip(observation_dates, temperature_observations))
        
        return jsonify(most_active_dict)
        
        
@app.route("/api/v1.0/trip/<start_date>")       
def start_date (start): 
        
        session = Session(engine)
        
        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
        
        session.close()
        
        tobs_values = []
        
        for min, max, avg in results:
            values = {}
            values["min"] = min
            values["max"] = max
            values["average"] = avg
            tobs_values.append(values)
        
        return jsonify(tobs_values)
        

@app.route("/api/v1.0/<start>/<end>")
def start_end_date (start, end):
        
        session = Session(engine)
        
        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        
        session.close()
        
        tobs_values = []
        
        for min, max, avg in results:
            values = {}
            values["min"] = min
            values["max"] = max
            values["average"] = avg
            tobs_values.append(values)
        
        return jsonify(tobs_values)
        
if __name__ == '__main__':
    app.run(debug=True) 