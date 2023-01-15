# ID2223-Air_Quality_Project


Lab description:

The goal of the project is to build a scalable prediction service using machine learning.

You can decide on the prediction service you want to build and identify the data source for that service (it must be a data source that is regularly updated, so your prediction service can make regular predictions).


You need to:
1. identify a location for air quality predictions (not Stockholm or Kyiv)
1. collect historical weather and air quality data for that location ( just pm25 and pm10 are the "standard" measurements you find in most sensors. They are enough.)
1. train a model with acceptable performance (don’t use logistic regression - use
XGBoost as a baseline) that uses both historical weather data and air quality measurements to predict future air quality (using future weather predictions)
1. build a Hugging Face space where you can see the predictions of air quality for that location for the next 7 days
> Sample code:
> https://github.com/logicalclocks/hopsworks-tutorials/tree/master/advanced_tutorials/air_quality



Deliver your project architecture and description as a README.md file in
the root of your Git repository.
1. Include in the README.md file:
1. a description of your prediction service its the data source
1. a public URL for the UI for your project (e.g., a Hugging Face Spaces URL).

## Deadline midnight 15th January.


