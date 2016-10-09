# Copy this file and name it ProtoConfig.py this is just an example it will not
# run without you renaming and filling out all fields with FILL IN.

import proto_out.config_pb2 as config_pb2

rootUrl = 'https://us.wio.seeed.io/v1/node/'
wiolinkAccessToken = 'FILL IN your access token'
wiolinkApiKey = '?access_token=' + wiolinkAccessToken
# Examples: Linux '/dev/ttyACM0', Windows 'COM5'
comPort = 'FILL IN your usb port'

# Get Config pbs for WioLinks and Arduions
def getConfig():
  wioLinks = {
  # WioLink name doesn't have to match actual name, it is just used by the
  # server to have a nice name for when you are parsing your configs.
  'FILL IN WioLink name': config_pb2.WioLinkConfig(rootUrl=rootUrl, apiKey=wiolinkApiKey,
    sensors={
    # Sensor name is a nice name for when you are parsing your configs.
    # apiMethod comes from your device go to
    # https://us.wio.seeed.io/v1/node/resources/[wiolinkApiKey] in a browser to
    # find these methods.
    'FILL IN sensor name' : config_pb2.GroveSensor(apiMethod='FILL IN api method'),
    # Examples:
    'airquality': config_pb2.GroveSensor(apiMethod='GroveAirqualityA0/quality'),
    'barometer': config_pb2.GroveSensor(apiMethod='GroveBaroBMP280I2C0/pressure'),
    'shaked': config_pb2.GroveSensor(apiMethod='GroveAccMMA7660I2C0/shaked'),
    }),
   # This is a map so feel free to add another device
  }
  arduinos = [config_pb2.ArduinoConfig(comPort=comPort, baudRate=9800)]
  return config_pb2.ServerConfig(wioLinks=wioLinks, arduinos=arduinos)
