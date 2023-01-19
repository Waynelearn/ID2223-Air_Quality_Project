import os
import modal
from Weather_API_utility import WeatherAPI
from Drawing import *

LOCAL=True
def weather_feature_engineering(df):
    #drop columns
    temp=df.copy()
    drop=["datetimeEpoch",
          "preciptype","snowdepth","sunrise",
          "sunset","icon","stations","source",
          "description","conditions"]
    temp=temp.drop(drop,axis=1)
    return temp

def update_mapping(new,d):
    temp=d.copy()
    for i in range(7,1,-1):
        temp[i]=temp[i-1]
    temp[1]=new
    return temp

if LOCAL == False:
   stub = modal.Stub("aqi_prediction")
   hopsworks_image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","scikit-learn","dataframe-image","xgboost"])
   @stub.function(image=hopsworks_image, secret=modal.Secret.from_name("lab1"))
   def f():
       g()

def g():
    import pandas as pd
    import hopsworks
    import joblib
    import datetime
    import numpy as np
    import pytz

    project = hopsworks.login(project="test42")
    fs = project.get_feature_store()

    mr = project.get_model_registry()
    model = mr.get_model("aqi_model_modal", version=1)
    model_dir = model.download()
    model = joblib.load(model_dir + "/aqi_model.pkl")
    print("Model loaded")

    weather_api="F5B6R3DHJAYYTDG9XVLMMHRBR"
    lat=1.3521
    lng=103.8198
    unitGroup="metric"
    include="days"

    w=WeatherAPI(weather_api,lat,lng,unitGroup,include)

    weather_input=w.forcast_query(7)
    weather_input=weather_feature_engineering(weather_input)
    
    date_lst=weather_input.datetime.values.tolist()

    weather_input=weather_input.drop("datetime",axis=1)
    weather_list=weather_input.values.tolist()
    


    fg = fs.get_or_create_feature_group(
        name="aqi",
        version=1,
        primary_key=['datetime','aqi'], 
        description="aqi")
    aqi_raw=fg.read()
    aqi_raw=aqi_raw.sort_values(by="datetime")

    last_7_days_aqi=aqi_raw.tail(7)["aqi"]
    last7dayslst=last_7_days_aqi.values.tolist()


    mapping = dict(zip([i for i in range(1,8)],last7dayslst))

    curr_aqi=list(mapping.values())
    curr_x=weather_list[0]
    curr_x.extend(curr_aqi)

    curr_x=np.array([curr_x])

    res=[]
    pred=model.predict(curr_x)[0]
    res.append(pred)
    mapping=update_mapping(pred,mapping)
    for i in range(1,7):
        curr_aqi=list(mapping.values())
        curr_x=weather_list[i]
        curr_x.extend(curr_aqi)
        curr_x=np.array([curr_x])
        pred=model.predict(curr_x)[0]
        res.append(pred)
        mapping=update_mapping(pred,mapping)

    final=pd.DataFrame({"datetime":date_lst,"aqi":res})

    print("Predictions for AQI:",final)
    print("UTC time:",datetime.datetime.utcnow())
    print("Singapore time", datetime.datetime.now(pytz.timezone('Asia/Singapore')))

    #L = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    #print(L)
    create_image_with_values(final)

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
       with stub.run():
            f()
