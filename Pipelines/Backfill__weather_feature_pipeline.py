import modal
import pandas as pd

LOCAL=False

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

    

"""
    backfill_weather=fs.get_or_create_feature_group(
        name="historical_weather",
        version=1,
        primary_key=[########],
        description="weather data for the past month"
        )
    back_fill_weather.insert(weather_data, write_options={"wait_for_job":False})
"""

if __name__ == "__main__":
    if LOCAL==True:
        g()
    else:
        with stub.run():
            f()
