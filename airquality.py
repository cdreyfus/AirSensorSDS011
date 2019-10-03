import serial, time
from Adafruit_IO import Client, RequestError, Feed

ADAFRUIT_IO_USERNAME = "cdreyfus"
ADAFRUIT_IO_KEY = "06b7f43809114d29b84f33a0963d7189"

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
baudrate = 9600
ser = serial.Serial('/dev/ttyUSB0', baudrate)

def create_feed_if_not_exist(feed_name):
    global feed_to_create
    try:
        feed_to_create = aio.feeds(feed_name)
    except RequestError:  # Doesn't exist, create a new feed
        feed = Feed(name=feed_name)
        feed_to_create = aio.create_feed(feed)

create_feed_if_not_exist("pmtwofive")
create_feed_if_not_exist("pmten")

while True:
    msg = ser.read(10)

    pm25 = (msg[3] * 256 + msg[2]) / 10.0
    pm10 = (msg[5] * 256 + msg[4]) / 10.0

    print('pmtwofive = %s μ/m^3' % pm25)
    print('pmten = %s μ/m^3' % pm10)
  
    aio.send('pmtwofive', pm25)
    aio.send('pmten', pm10)
    
    time.sleep(10)
