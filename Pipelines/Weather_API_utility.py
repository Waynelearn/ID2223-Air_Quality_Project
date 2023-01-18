import urllib.request
import datetime
import json
import pandas as pd

class WeatherAPI:
    def __init__(self,API_KEY,lat,lng,unitGroup,include):
        self.base_url="https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        self.API_KEY=API_KEY
        self.lat=lat
        self.lng=lng
        self.unitGroup=unitGroup
        self.include=include
      
    def from_to_url(self,start,end):
        return f"{self.base_url}/{self.lat},{self.lng}/{start}/{end}?&unitGroup={self.unitGroup}&include={self.include}&key={self.API_KEY}"

    def forcast_url(self,n_days):
        #not including today
        start=datetime.date.today()+datetime.timedelta(days=1)
        end=start+datetime.timedelta(days=n_days-1)
        start=start.strftime("%Y-%m-%d")
        end=end.strftime("%Y-%m-%d")
        return self.from_to_url(start,end)

    def historical_url(self,n_days):
        #not including today
        end=datetime.date.today()-datetime.timedelta(days=1)
        start=end-datetime.timedelta(days=n_days-1)
        start=start.strftime("%Y-%m-%d")
        end=end.strftime("%Y-%m-%d")
        return self.from_to_url(start,end)

    def query(self,url):
        data=urllib.request.urlopen(url)
        json_data=json.loads(data.read())
        df=pd.DataFrame(json_data["days"])
        return df

    def forcast_query(self,n_days):
        return self.query(self.forcast_url(n_days))

    def historical_query(self,n_days):
        return self.query(self.historical_url(n_days))

    def from_to_query(self,start,end):
        return self.query(self.from_to_url(start,end)



if __name__=="__main__":
    base_url="https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
    weather_api="F5B6R3DHJAYYTDG9XVLMMHRBR"
    lat=1.3521
    lng=103.8198
    unitGroup="metric"
    include="days"
    
    test=WeatherAPI(weather_api,lat,lng,unitGroup,include)
    #print(test.forcast_url(7))
    #test.query(test.historical_url(2)).to_csv("test.csv")
