#!/usr/bin/python3

# I know it doesn't work without the api_key. I just don't know how to include it without writing it in the code or another file.
# currently the key is in another file on my pc and I've tested it and it works

import paho.mqtt.client as mqtt
import time
import wetter
import datetime
import os
    
weather_api = wetter.OpenWeatherMapAPI()
location = {
    "lat" : 48.7758,
    "lon" : 9.1829,
}
    
def on_connect(client,userdata,flags, rc):
    #Hier sollten alle Topics aufgelistet werden, auf welche gehört werden soll
    #Der integer-Wert im Tuple ist egal, da er nicht von der Methode verwendet wird
    client.subscribe([("req/weather/now", 0),("req/weather/<Datum>/<Uhrzeit>", 0),("location/current", 0)])
    client.publish("req/location/current", 0)

#Diese Funktion wird aufgerufen, wenn es für ein Topic kein spezielles Callback gibt
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    

def specific_callback(client, userdata, msg):
    global location
    print("Specific Topic: "+msg.topic+" "+str(msg.payload))
    if msg.topic == "location/current":
       location = msg.payload
       return
    
    if msg.topic == "req/weather/now":
        #client.publish(weather_api.get_current_weather_by_city("Berlin"))
        client.publish("weather/now", weather_api.get_current_weather_with_gps(location["lat"], location["lon"]))
        print("sent weather/now")
        return
    
    if msg.topic == "req/weather/<Datum>/<Uhrzeit>":
        client.publish("weather/<Datum>/<Uhrzeit>", weather_api.get_weather_by_date_with_gps(location["lat"], location["lon"], msg.payload["date"] + " " + msg.payload["time"]))
        print("sent weather/<Datum>/<Uhrzeit>")
        return

if __name__ == "__main__": # pragma: no cover
    #aufbau der MQTT-Verbindung
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    #Definition einer Callback-Funktion für ein spezielles Topic
    client.message_callback_add("weather/now", specific_callback)
    client.message_callback_add("weather/<Datum>/<Uhrzeit>", specific_callback)
    client.message_callback_add("location/current", specific_callback)
    #weather/now
    #weather/<Datum>/<Uhrzeit>

    docker_container = os.environ.get('DOCKER_CONTAINER', False)
    if docker_container:
        mqtt_address = "broker"
    else:
        mqtt_address = "localhost"
    client.connect(mqtt_address,1883,60)
    client.loop_start()

    #Hier kann der eigene Code stehen. Loop oder Threads    
    while True:
        time.sleep(100)
        #client.publish("test/Pfad/1", "asdf")

    #Sollte am Ende stehen, da damit die MQTT-Verbindung beendet wird
    client.loop_stop()
    client.disconnect()

