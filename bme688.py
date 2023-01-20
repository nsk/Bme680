import time
import board
import adafruit_bme680
import paho.mqtt.client as mqtt

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

#create mqtt client
client = mqtt.Client(client_id="your id")

#set username and password
client.username_pw_set(username="login",password="yourpass")

#connect to the broker
client.connect("yourip", port=1883, keepalive=60)

# check if the connection is successful
if client.connect_status:
    print("Connection Successful")
else:
    print("Connection Failed")

#start the loop
client.loop_start()

# AIQ table
AIQ_table = {
    0: "Excellent",
    500: "Good",
    1000: "Fair",
    1500: "Poor",
    2000: "Unhealthy"
}

while True:
    # get the VOC resistance value
    voc_resistance = bme680.gas_resistance

    # initialize air quality to the last level
    air_quality = "Unhealthy"

    # find the closest air quality level
    for level in sorted(AIQ_table.keys()):
        if voc_resistance > level:
            air_quality = AIQ_table[level]
        else:
            break

    print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)
    print("VOC resistance: %d ohm" % bme680.gas_resistance)
    print("Air Quality: %s" % air_quality)

    client.publish("topic",payload= "Temperature: %0.1f C" % (bme680.temperature + temperature_offset))
    client.publish("topic",payload= "Gas: %d ohm" % bme680.gas)
    client.publish("topic",payload= "Humidity: %0.1f %%" % bme680.relative_humidity)
    client.publish("topic",payload= "Pressure: %0.3f hPa" % bme680.pressure)
    client.publish("topic",payload= "Altitude = %0.2f meters" % bme680.altitude)
    client.publish("topic",payload= "VOC resistance: %d ohm" % bme680.gas_resistance)
    client.publish("topic",payload= "Air Quality: %s" % air_quality)
    
    time.sleep(1)
