# sqlalchemy-challenge

* In this repo, the folder SurfsUp contains the main jupyter notebook script for analysis and the python script for the app.
* The folder Resources contains the document and sheets used for the analysis and the IMages folder contains the output of the analysis.

# Summary

* Python and SQLAlchemy was used to do a basic climate analysis and data exploration of the climate database provided.

## Precipitation Analysis
* Find the most recent date in the dataset.
* Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
* Select only the "date" and "prcp" values.
* Load the query results into a Pandas DataFrame, and set the index to the "date" column.
* Sort the DataFrame values by "date".
* Plot the results by using the DataFrame plot method.
* Use Pandas to print the summary statistics for the precipitation data.

## Station Analysis
* Design a query to calculate the total number of stations in the dataset.
* Design a query to find the most-active stations (that is, the stations that have the most rows).
* Using the most-active station id, calculate the lowest, highest, and average temperatures.
* Design a query to get the previous 12 months of temperature observation (TOBS) data for the most-active station.
* Plot the results as a histogram with bins=12.

## Design Climate App
* Design a Flask API based on the queries
* List all the available routes on homepage.
* Return the JSON representation of percipitation data.
* Return a JSON list of stations from the dataset.
* Return a JSON list of temperature observations for the previous year for the most-active station.
* Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
