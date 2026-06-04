
import httpx

class Api_Weather:
    def __init__(self,api_key,timeout=5):
        self.api_client=httpx.Client(base_url='http://api.openweathermap.org',
                                     timeout=timeout)
        self.api_key=api_key

    def weather_by_coordinates(self,lat,lon,units='metric',exclude='hourly'):
        params={
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': units,
            'exclude': exclude
        }
        response=self.api_client.get(f'data/2.5/weather?lat=",latitude,"&lon=",longitude,"&appid=",{API_KEY},"&units=metric"',params=params)
        print(response.json())
        print(response)
        return response

    def weather_by_city_name(self,city_name,limit=1,units='metric'):
        params={
            'q':city_name,
            'limit':limit,
            'appid':self.api_key,
            'units':units
        }
        response=self.api_client.get(f'data/2.5/weather',params=params)
        print(response.json())
        print(response)
        return response

    def weather_by_timestamps(self,lat,lon,cnt=40,units='metric'):
        params={
            'lat':lat,
            'lon':lon,
            'cnt':cnt,
            'appid':self.api_key,
            'units':units
        }
        response=self.api_client.get('data/2.5/forecast',params=params)
        print(response.json())
        print(response)
        return response



API_KEY='acb6181d90f7e5c5290112926d4eeb1f'
weather=Api_Weather(api_key=API_KEY)
weather.weather_by_coordinates( 51.12,71.43,'metric') # Казахстан/Астана(Нурсултан)

response = weather.weather_by_city_name('Sofia') # Болгария/София
print(response.status_code)  # 200
print(response.json()['sys']['country'])
response=weather.weather_by_timestamps( 54.71,20.51,24,'metric') # Россия/Калининград


















