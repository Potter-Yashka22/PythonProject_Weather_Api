import allure
import pytest

from src.api.weather import Api_Weather, response

@pytest.fixture
def weather_api():
    api_key="acb6181d90f7e5c5290112926d4eeb1f"
    return Api_Weather(api_key=api_key)
@pytest.mark.api
@allure.epic('Тестирую api openweather') # вот эта штука у меня почему-то не отрабатывает
@allure.feature('тесты погоды по геометкам/позитивные')
@allure.story('Тесты с параметризацией')
@pytest.mark.parametrize('lat,lon,name',[
    (41.72,44.78, 'Saburtalo'),
    (69.33,88.22,"Noril'sk"),
    (41.90,12.50, 'Trevi')
])
def test_weather_by_coordinates(weather_api,lat,lon,name):
    # lat,lon=51.12,71.43
    response=weather_api.weather_by_coordinates(lat,lon,name)
    with allure.step('проверяем статус код, 200'):
        assert response.status_code==200
    data=response.json()
    with allure.step('пытаюсь убедиться что названия городов по координатам соответствуют задуманным'):
        assert data['name']==name
    assert 'lat' in str(response.json()) or 'current' in str(response.json())
    assert 'temp' in str(data) or 'temperature' in str(data)
    with allure.step('Проверяю что параметр id присутствует в ответе'):
        assert response.json()['id']
    assert isinstance(response.json()['id'],int)
@pytest.mark.api
@allure.feature('тесты погоды по геометкам/позитивные')
@allure.story('Тесты погоды по названию города')
def test_weather_by_city_name(weather_api):
    response=weather_api.weather_by_city_name('Sofia')
    with allure.step('проверяем статус код, 200'):
        assert response.status_code==200
    data=response.json()
    for key,value in data.items():
        print(f"{key}:{value}")
    with allure.step('проверяем что ключ name соответствует заданному'):
        assert data['name']=='Sofia'
    with allure.step('проверяем что ключ country соответствует заданному'):
        assert data['sys']['country']=='BG'
    assert 'main' in data
    assert 'temp' or 'temperature' in data['main']
@pytest.mark.api
@allure.feature('тесты погоды по геометкам/позитивные')
@allure.story('Тесты прогноз погоды с шагом в 3 часа в Калининграде на сутки')
def test_weather_by_timestamps(weather_api):
    lat,lon=54.71,20.51 # Калининград
    response=weather_api.weather_by_timestamps(lat,lon,cnt=40)
    with allure.step('проверяем статус код, 200'):
        assert response.status_code==200
    data=response.json()
    for key,value in data.items():
        print(f"{key}:{value}")
    with allure.step('проверяем что ключ list присутствует в данных'):
        assert 'list' in data
    with allure.step('проверяем количество точек прогноза'):
        assert len(data['list'])==40
    first_forecast=data['list'][0]
    with allure.step('проверяем наличие ключевых значений в данных'):
        assert 'dt' in first_forecast
    with allure.step('проверяем наличие ключевых значений в данных'):
        assert 'main' in first_forecast
    with allure.step('проверяем наличие ключевых значений в данных'):
        assert 'temp' in first_forecast['main']
    with allure.step('проверяем наличие ключевых значений в данных'):
        assert 'weather' in first_forecast
    print(f"Город: {data['city']['name']}")
    print(f"Количество точек прогноза: {len(data['list'])}")
    print("\nПрогноз на ближайшие сутки: ")
    for i in range(9):
        forecast=data['list'][i]
        print(f" {forecast['dt_txt']}: {forecast['main']['temp']}°C")
@pytest.mark.api
@allure.feature("Тесты по геометкам")
@allure.story("Негативные сценарии")
@allure.title("Поиск погоды по несуществующему городу → ошибка 404")
def test_weather_by_city_name_negative(weather_api):
    response=weather_api.weather_by_city_name('NonExistentCityQWErty123')
    with allure.step('проверяем статус код, 404'):
        assert response.status_code==404
    assert response.json()['cod']=='404'
@pytest.mark.api
@allure.feature("Тесты по геометкам")
@allure.story("Негативные сценарии")
@allure.title("Поиск погоды с пустым запросом  → ошибка 404")
def test_weather_by_city_name_empty_str(weather_api):
    response=weather_api.weather_by_city_name('')
    with allure.step('проверяем статус код, 400'):
        assert response.status_code==400 or response.status_code==404






















