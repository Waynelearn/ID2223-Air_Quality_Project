import os
import modal
from Weather_API_utility import *
LOCAL=False
def weather_feature_engineering(df):
    #drop columns
    temp=df.copy()
    drop=["datetimeEpoch",
          "preciptype","snowdepth","sunrise",
          "sunset","icon","stations","source",
          "description","conditions"]
    temp=temp.drop(drop,axis=1)
    return temp

if LOCAL == False:
   stub = modal.Stub("daily-weather")
   image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","scikit-learn","beautifulsoup4"]) 

   @stub.function(image=image, schedule=modal.Cron("59 15 * * *"), secret=modal.Secret.from_name("lab1"))
   def f():
       g()





def g():
    import hopsworks
    import pandas as pd
    import datetime

    project = hopsworks.login(project="test42")
    fs = project.get_feature_store()

    remain=['datetime', 'tempmax', 'tempmin', 'temp', 'feelslikemax',
       'feelslikemin', 'feelslike', 'dew', 'humidity', 'precip', 'precipprob',
       'precipcover', 'snow', 'windgust', 'windspeed', 'winddir', 'pressure',
       'cloudcover', 'visibility', 'solarradiation', 'solarenergy', 'uvindex',
       'severerisk', 'sunriseEpoch', 'sunsetEpoch', 'moonphase']
    weather_api="F5B6R3DHJAYYTDG9XVLMMHRBR"
    lat=1.3521
    lng=103.8198
    unitGroup="metric"
    include="days"
    w=WeatherAPI(weather_api,lat,lng,unitGroup,include)
    

    df = w.today_query()#1 data point
    df = weather_feature_engineering(df)
    #df["datetime"]=df["datetime"].apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))

    weather=fs.get_or_create_feature_group(
        name="historical_weather",
        version=1,
        primary_key=remain,
        description="weather data for the past month"
        )
    weather.insert(df, write_options={"wait_for_job":False})


if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
       stub.deploy("daily-weather")
       with stub.run():
            f()
