#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time
import os
    
def on_connect(client,userdata,flags, rc):
    #Hier sollten alle Topics aufgelistet werden, auf welche gehört werden soll
    #Der integer-Wert im Tuple ist egal, da er nicht von der Methode verwendet wird
    client.subscribe([("weather/now", 0),("weather/<Datum>/<Uhrzeit>", 0)])

#Diese Funktion wird aufgerufen, wenn es für ein Topic kein spezielles Callback gibt
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == "__main__": # pragma: no cover
    #aufbau der MQTT-Verbindung
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    docker_container = os.environ.get('DOCKER_CONTAINER', False)
    if docker_container:
        mqtt_address = "broker"
    else:
        mqtt_address = "localhost"
    client.connect(mqtt_address,1883,60)
    client.loop_start()

    #Hier kann der eigene Code stehen. Loop oder Threads    
    while True:
        client.publish("req/weather/now", 0)
        print("tried request")
        time.sleep(30)
        #client.publish("test/Pfad/1", "asdf")

    #Sollte am Ende stehen, da damit die MQTT-Verbindung beendet wird
    client.loop_stop()
    client.disconnect()

