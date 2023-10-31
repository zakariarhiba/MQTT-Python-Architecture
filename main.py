# import library 
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox
from PyQt5 import uic,QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys

#Import the paho Library : 
import paho.mqtt.client as paho
#this is a thread responsible of the connection with the broker
class MqttApp(QThread):
	temp = pyqtSignal(str) # this is the signal that goanna recieve the value of the temperature

	# Function of handling the Mqtt parameters necessary for the broker
	def run(self):
		self.client = paho.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.on_publish = self.on_publish
		self.client.connect("test.mosquitto.org", 1883, 60)
		self.client.loop_forever()

	# when connect success to the broker, subsciber to the topic
	def on_connect(self, client, userdata, flags, rc):
		self.client.subscribe("SmartApplication/temperature")

	# when the value's goanna received we goanna stock it on the temperature signal
	# the from the signal we goanna show it on the main window LCD Number
	def on_message(self, client, userdata, msg):
		topic, message = msg.topic, msg.payload.decode("utf-8")
		print(topic + " -> " + str(message))
		if topic == "SmartApplication/temperature":
			self.temp.emit(str(message))

	# This is the function when we goanna send the commands of the LED to turn on or Off
	def publish_msg(self, topic, message):
		ret = self.client.publish(topic, message)

	def on_publish(self, client, userdata, result):
		print("data published")




# initialize the MainWindow of our app
class Main(QMainWindow):
	def __init__(self):
		# call init of QMainWindow
		super().__init__()
		# load our design from Qtdesigner 
		uic.loadUi('./main.ui', self) 
		# set up our app functionality 
		self.set_ui()
		self.buttons()
		self.start_subscribing() # calling the mqtt thread function

	# those two functions are responsible of handling the temperature signal 
	# to show in the main window, it takes the value from the MQTT thread then it rewrite it 
	# in the main window and then to the LCD Number widget box
	def start_subscribing(self):
		self.thread = MqttApp()
		self.thread.temp.connect(self.set_temp) # receiving the temperature value
		self.thread.start()
	def set_temp(self, temp):
		self.lcd_temperature.display(temp) # this line responsible of LCD Number change value

	def set_ui(self):
		self.setWindowTitle('Smart Application') #This is the title of our App
		self.setFixedSize(770,552)  # This is the size of our Application in the System
        
	#This is the function where we goanna set the trigged of our push Buttons
	def buttons(self):
		# those buttons where are clicked the use the Mqtt thread publish function to 
		# send 0 or 1 to the broker to control the led.
		self.led_on.clicked.connect(lambda: self.thread.publish_msg("SmartApplication/LED", "1"))
		self.led_off.clicked.connect(lambda: self.thread.publish_msg("SmartApplication/LED", "0"))

	
        



# if code run from main
if __name__ == '__main__':
	    # create app in sys
    app = QApplication(sys.argv)
    # load our MainWindow 
    main = Main()
    # show the window 
    main.show()

     # except end process
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Clossing window...')

