import modal
import pandas as pd
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
    
    #change datetime col to datetime datatype
    df["datetime"]=df["datetime"].apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    
if LOCAL==False:
    stub=modal.Stub()
    image=modal.Image.debian_slim().pip_install(["hopsworks","joblib"])

    @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("lab1"))
    def f():
        g()
def g():
    import hopsworks
    import pandas as pd

    project=hopsworks.login(project="test42")
    fs=project.get_feature_store()

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
    #get the past 40 days of weather data
    weather_data=w.historical_query(40)
    weather_data=weather_feature_engineering(weather_data)

    

    backfill_weather=fs.get_or_create_feature_group(
        name="historical_weather",
        version=1,
        primary_key=remain,
        description="weather data for the past month"
        )
    backfill_weather.insert(weather_data, write_options={"wait_for_job":False})


if __name__ == "__main__":
    if LOCAL==True:
        g()
    else:
        with stub.run():
            f()
