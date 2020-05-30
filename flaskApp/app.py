from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# Get current conditions from WeatherLink API and return as Json Object
def getCurrentConditions():
    currentConditions = requests.get("http://10.0.0.5/v1/current_conditions")
    if currentConditions.status_code == 200:
        return json.loads(currentConditions.text)
    return "-1"

def chooseThermometerIcon(currentConditions):
    temp = currentConditions['data']['conditions'][0]['temp']
    #These temp ranges are completely arbitrary :-)
    if temp > 85:
        return "fa-thermometer-three-full"
    elif temp > 45 and temp < 85 :
        return "fa-thermometer-three-quarters"
    elif temp > 32 and temp < 45 :
        return "fa-thermometer-three-half"
    else:
        return "fa-thermometer-three-quarter"


#Provide a Human Redable Compass Direction for a given degree heading
def windDirection(directionInDegrees):
    if directionInDegrees > 360 or directionInDegrees < 0:
        return "Error"
    elif 348.75 <= directionInDegrees <= 360 or  0.00 <= directionInDegrees < 11.25:
        return "N"
    elif 11.25 <= directionInDegrees < 33.75:
        return "NNE"
    elif 33.75 <= directionInDegrees < 56.25:
       return "NE"
    elif 56.25 <= directionInDegrees < 78.75:
       return "ENE"
    elif 78.75 <= directionInDegrees < 101.25:
       return "E"
    elif 101.25 <= directionInDegrees < 23.75:
       return "ESE"
    elif 123.75 <= directionInDegrees < 146.25:
       return "SE"
    elif 146.25 <= directionInDegrees < 168.75:
       return "SSE"
    elif 168.75 <= directionInDegrees < 191.25:
       return "S"
    elif 191.25 <= directionInDegrees < 213.75:
       return "SSW"
    elif 213.75 <= directionInDegrees < 236.25:
       return "SW"
    elif 236.25 <= directionInDegrees < 258.75:
       return "WSW"
    elif 258.75 <= directionInDegrees < 281.25:
       return "w"
    elif 281.25 <= directionInDegrees < 303.75:
       return "WNW"
    elif 303.75 <= directionInDegrees < 326.25:
       return "NW"
    elif 326.25 <= directionInDegrees < 348.75:
       return "NNW"

@app.route("/")
def index():
    currentConditions = getCurrentConditions()
    if currentConditions == "-1":
        return render_template("serverError.html")

    return render_template("index.html", 
                            temp=currentConditions['data']['conditions'][0]['temp'],
                            thermometerIcon=chooseThermometerIcon(currentConditions),
                            hum=currentConditions["data"]["conditions"][0]["hum"],
                            dew_point=currentConditions['data']['conditions'][0]['dew_point'],
                            heat_index=currentConditions['data']['conditions'][0]['heat_index'],
                            wind_chill=currentConditions['data']['conditions'][0]['wind_chill'],
                            wind_speed_avg_last_1_min=currentConditions["data"]["conditions"][0]["wind_speed_avg_last_1_min"],
                            wind_dir_scalar_avg_last_1_min=currentConditions["data"]["conditions"][0]["wind_dir_scalar_avg_last_1_min"],
                            wind_dir=windDirection(currentConditions["data"]["conditions"][0]["wind_dir_scalar_avg_last_1_min"]),
                            wind_speed_hi_last_10_min=currentConditions["data"]["conditions"][0]["wind_speed_hi_last_10_min"]
                          )


@app.route("/error")
def error():
    return render_template("404.html")