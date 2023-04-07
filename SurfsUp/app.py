# Import the dependencies.
from flask import Flask, jsonify
import json
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func, create_engine


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///sunshine.sqlite")
engine = create_engine(f"postgresql://postgres:password@localhost/Module 10 Challenge")
Base = automap_base()
Base.prepare(autoload_with=engine)
# store the reference to the measurement table
Measurement = Base.classes.measurement
Station = Base.classes.station

# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################


app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    print("Server attempted to go to home page....") # prints in output console
    return ("Homepage for GT Boot Camp Module 10 Challenge!<br>"
            "<br>"
            "<b>-------------------------<br>"
            f"Current Routes <br>"
            f"-------------------------</b><br>"
            f"/ <br>"
            f"/about<br>"
            f"/contact<br>"
            f"/api/v1.0  - Surf Data App<br>")

@app.route("/about")
def about():
    name = "Jason Hanlin"
    email = "jason@cte.tv"
    return f"My name is {name} and my email address is {email}"

#################################################
# make a sqlalchemy route for surfdata landing page
@app.route("/api/v1.0")
def surfdata():
    return ("This is an app to get Surf Data<br>"
            "<br>"
            "<b>-------------------------<br>"
            f"Current Routes <br>"
            f"-------------------------</b><br>"
            f"/ <br>"
            f"/precipitation  - last 12 months of precipitation data for the most active station for data collection<br>"
            f"/station  - station information including ID, station name, latitude, longitude, elevation<br>"
            f"/start date  - enter start date in yyyy-mm-dd format to get min, max, and average data for the period following the start date<br>"
            f"/start date/end date  - enter start date and end date in yyyy-mm-dd format to get min, max, and average data for the period between start and end dates<br>")


#################################################
# Make a sqlalchemy route for Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

@app.route("/api/v1.0/precipitation")
def precipitation():
    
 # create the session
    session = Session(engine)

    prcp_query = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date > '2016-08-23').\
                order_by(Measurement.date).all()

    # make an empty list and store the dictionaries
    resultList = []
    for result in prcp_query:
        resultDict = {}
        resultDict["date"] = result["date"]
        resultDict["prcp"] = result["prcp"]
        resultList.append(resultDict)
    # jsonify and display the contents in the list
    return jsonify(resultList)


#################################################
# make a sqlalchemy route for station information
@app.route("/api/v1.0/station")
def stationData():
    # create the session
    session = Session(engine)
    # query all station data
    results = session.query(Station.id,
                            Station.station,
                            Station.name,
                            Station.latitude,
                            Station.longitude,
                            Station.elevation).all()
    # make an empty list and store the dictionaries
    resultList = []
    for result in results:
        resultDict = {}
        resultDict["id"] = result["id"]
        resultDict["station"] = result["station"]
        resultDict["name"] = result["name"]
        resultDict["latitude"] = result["latitude"]
        resultDict["longitude"] = result["longitude"]
        resultDict["elevation"] = result["elevation"]
        resultList.append(resultDict)
    # use np.ravel() to turn the tuple into a normal list
    #allResults = list(np.ravel(results))
    # jsonify and display the contents in the list
    return jsonify(resultList)


#################################################
# Make a sqlalchemy route for a query of the dates and temperature observations of the most-active station 
# for the previous year of data

@app.route("/api/v1.0/tobs")
def tobs():
    
 # create the session
    session = Session(engine)

    tobs_query = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > '2016-08-19').\
            order_by(Measurement.date).all()

    # make an empty list and store the dictionaries
    resultList = []
    for result in tobs_query:
        resultDict = {}
        resultDict["date"] = result["date"]
        resultDict["tobs"] = result["tobs"]
        resultList.append(resultDict)
    # jsonify and display the contents in the list
    return jsonify(resultList)


#################################################
# Make a sqlalchemy route for a query of the dates and temperature observations of the most-active station 
# for the previous year of data

@app.route("/api/v1.0/<start>")
def start(start):
    
 # create the session
    session = Session(engine)

    tmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).first()
    tmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).first()
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).first()

#    return f'tmax is {tmax}'

    tempresults = {
    "tmax": tmax[0],
    "tmin": tmin[0],
    "tavg": tavg[0]
}

    return jsonify(tempresults)

#################################################
# Make a sqlalchemy route for a query of the dates and temperature observations of the most-active station 
# for the previous year of data

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
 # create the session
    session = Session(engine)

    tmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(start, end)).first()
    tmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(start, end)).first()
    tavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date.between(start, end)).first()

    tempresults = {
    "tmax": tmax[0],
    "tmin": tmin[0],
    "tavg": tavg[0]
}

    return jsonify(tempresults)




#-----------------------------------------------#
# name of the application in order to start from command line
if __name__ == "__main__":
    app.run(debug=True) # module used to start the development server
            # to stop the server, use ctrl+c or cmd+c



