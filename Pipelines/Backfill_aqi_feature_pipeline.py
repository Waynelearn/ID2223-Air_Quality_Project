import pandas as pd
import modal
import datetime

LOCAL=False

if LOCAL==False:
    stub=modal.Stub()
    image=modal.Image.debian_slim().pip_install(["hopsworks","joblib"])

    @stub.function(image=image, secret=modal.Secret.from_name("lab1"))
    def f():
        g()

def g():
    import hopsworks
    import pandas as pd

    project=hopsworks.login(project="test42")
    fs=project.get_feature_store()

    fg = fs.get_or_create_feature_group(
        name="aqi",
        version=1,
        primary_key=['datetime','aqi'], 
        description="aqi")
    df=pd.read_csv("https://raw.githubusercontent.com/Waynelearn/ID2223-Air_Quality_Project/main/Pipelines/aqi_data.csv",index_col=0)
    df["datetime"]=df["datetime"].apply(lambda x:datetime.datetime.strptime(x,"%d/%m/%Y"))
    df["datetime"]=df["datetime"].apply(lambda x:x.strftime("%Y-%m-%d"))
    fg.insert(df, write_options={"wait_for_job" : False})

if __name__ == "__main__":
    if LOCAL==True:
        g()
    else:
        with stub.run():
            f()
