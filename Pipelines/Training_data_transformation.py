

def get_training_data():
    import pandas as pd
    import hopsworks
    
    project=hopsworks.login(project="test42")
    fs=project.get_feature_store()

    remain=['datetime', 'tempmax', 'tempmin', 'temp', 'feelslikemax',
           'feelslikemin', 'feelslike', 'dew', 'humidity', 'precip', 'precipprob',
           'precipcover', 'snow', 'windgust', 'windspeed', 'winddir', 'pressure',
           'cloudcover', 'visibility', 'solarradiation', 'solarenergy', 'uvindex',
           'severerisk', 'sunriseEpoch', 'sunsetEpoch', 'moonphase']

    weather=fs.get_or_create_feature_group(
            name="historical_weather",
            version=1,
            primary_key=remain,
            description="weather data for the past month"
            )
    weather_df=weather.read()

    aqi= fs.get_or_create_feature_group(
            name="aqi",
            version=1,
            primary_key=['datetime','aqi'], 
            description="aqi")

    aqi_df=aqi.read()

    aqi_df=aqi_df.sort_values(by="datetime")

    for i in range(1,8):
        aqi_df[f"aqi_{i}"]=aqi_df["aqi"].shift(i)

    aqi_df=aqi_df.dropna(subset=[f"aqi_{i}" for i in range(1,8)],how="any",axis="rows")

    
    combined_data=weather_df.merge(aqi_df,on="datetime", how="right")

    return combined_data
if __name__=="__main__":
    print(get_training_data())
