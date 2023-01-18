import os
import modal

LOCAL=False

if LOCAL == False:
   stub = modal.Stub("daily-aqi")
   image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","scikit-learn","beautifulsoup4"]) 

   @stub.function(image=image, schedule=modal.Cron("59 15 * * *"), secret=modal.Secret.from_name("lab1"))
   def f():
       g()





def g():
    import hopsworks
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    import datetime
    URL = "https://www.iqair.com/singapore"
    page = requests.get(URL)
    class_select="aqi-value__value"

    project = hopsworks.login(project="test42")
    fs = project.get_feature_store()

    #webscrapping from aqi website for aqi number once every day
    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.find(class_=class_select)
    result=int(result.contents[0])
    curr_date=datetime.date.today()
    curr_date=curr_date.strftime("%Y-%m-%d")
    

    df = pd.DataFrame({"datetime":[curr_date],"aqi":[result]})#1 data point
    #df["datetime"]=df["datetime"].apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))

    fg = fs.get_or_create_feature_group(
        name="aqi",
        version=1,
        primary_key=['datetime','aqi'], 
        description="aqi")
    fg.insert(df, write_options={"wait_for_job" : False})

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
       stub.deploy("daily-aqi")
       with stub.run():
            f()
