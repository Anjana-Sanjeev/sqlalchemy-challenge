# Import depedencies

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

# Database Setup

# Create engine to hawaii.sqlite

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model

Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)

# Find the most recent date in the data set

recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date one year from the last date in data set.

last_twelve_months = dt.datetime.strptime(recent_date[0], '%Y-%m-%d') - dt.timedelta(days = 365)

# Find the most active station

sel = [Measurement.station, func.count(Measurement.id)]

active_stations = session.query(*sel).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()

most_active_station = active_stations[0][0]

# Flask Setup

app = Flask(__name__)

# Display the available routes on the landing page

@app.route("/")

def welcome():
    
    return (
        f"Available Routes:<br/>"
        f"----------------------<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature data for last year for most active station (USC00519281): /api/v1.0/tobs<br/>"
        f"Temperature data from the start date (start date to be inputted in the url): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature data from start to end date (start and date to be inputted in the url): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

# Precipitation data for the last year

@app.route("/api/v1.0/precipitation")

def percipitation():

    session = Session(engine)
    sel = [Measurement.date, Measurement.prcp]
    date_prcp = session.query(*sel).filter(Measurement.date >= last_twelve_months).all()
    session.close()

    precipitation = []
    for date, prcp in date_prcp:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

# Data of all of the stations

@app.route("/api/v1.0/stations")

def stations():

    session = Session(engine)
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    station_data = session.query(*sel).all()
    session.close()

    stations = []
    for station,name,lat,lon,el in station_data:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

# Temperature observations of the most-active station for the previous year of data.

@app.route("/api/v1.0/tobs")

def tobs():
    session = Session(engine)
    sel = [Measurement.date, Measurement.tobs]
    temperature_data = session.query(*sel).filter(Measurement.station == most_active_station).filter(Measurement.date >= last_twelve_months).all()
    session.close()

    temperature = []
    for date, tobs in temperature_data:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["TOBS"] = tobs
        temperature.append(tobs_dict)

    return jsonify(temperature)

# Temperature data from the given start date

@app.route("/api/v1.0/<start>")

def start_date(start):

    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    start_date_TOBS = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= recent_date[0]).all()
    session.close()

    start_TOBS = []
    for min, max, avg in start_date_TOBS:
        start_tobs_dict = {}
        start_tobs_dict["T_Min"] = min
        start_tobs_dict["T_Max"] = max
        start_tobs_dict["T_Average"] = avg
        start_TOBS.append(start_tobs_dict)

    return jsonify(start_TOBS)

# Temperature data from the given start date to end date

@app.route("/api/v1.0/<start>/<end>")

def start_end_date(start, end):

    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    start_end_date_TOBS = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    start_end_TOBS = []
    for min, max , avg in start_end_date_TOBS:
        start_end_tobs_dict = {}
        start_end_tobs_dict["T_Min"] = min
        start_end_tobs_dict["T_Max"] = max
        start_end_tobs_dict["T_Average"] = avg
        start_end_TOBS.append(start_end_tobs_dict)

    return jsonify(start_end_TOBS)

if __name__ == "__main__":
    app.run(debug = True)