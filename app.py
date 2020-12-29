from flask import Flask, request, render_template
import requests


app = Flask(__name__)

@app.route('/get_lowest_temp')
def get_weather():
    API_KEY = '4f6ba86016ff1332409b755f3839bfb6'
    cities = ["Tel-Aviv", "Berlin", "Budapest"]
    result = {}
    #for each city - find its data-entry with the lowest temperature measured
    for city in cities:
        url = "http://api.openweathermap.org/data/2.5/forecast?q={}&&units=metric&appid={}".format(city, API_KEY)
        r = requests.get(url)
        r_json = r.json()
        min_temperature = r_json["list"][0]["main"]["temp_min"]
        city_data = r_json["list"][0]["main"]
        for entry in r_json["list"]:
            if entry["main"]["temp_min"] <= min_temperature:
                min_temperature = entry["main"]["temp_min"]
                city_data = entry["main"]
        result[city] = city_data
    print(result)

    #result contain the lowest temp and data measured for each of the cities
    #the following code will return the city with the lowest temp measured among the 3 (and its data)
    coldest_temperature = result["Tel-Aviv"]["temp_min"]
    coldest_temperature_main = result["Tel-Aviv"]
    coldest_temperature_main["city"] = "Tel-Aviv"
    for city in result:
        if result[city]["temp_min"] < coldest_temperature:
            coldest_temperature = result[city]["temp_min"]
            coldest_temperature_main = result[city]
            coldest_temperature_main["city"] = city
    return coldest_temperature_main


@app.route('/')
def index():
    coldest_city = get_weather()
    return render_template("index.html", coldest_city=coldest_city)



if __name__ == '__main__':
    app.run(debug = True)