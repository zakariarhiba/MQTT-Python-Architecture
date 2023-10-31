import paho.mqtt.client as paho
from time import sleep

broker = "test.mosquitto.org"
port = 1883


def on_publish(client, userdata, result):  # create function for callback
    print("data published \n")


client1 = paho.Client("control1")  # create client object
client1.on_publish = on_publish  # assign function to callback
client1.connect(broker, port)

while True:
    ret = client1.publish("SmartApplication/temperature", 37)
    sleep(4)
    ret = client1.publish("SmartApplication/temperature", 38)
    sleep(4)
    ret = client1.publish("SmartApplication/temperature", 35)
    sleep(4)



