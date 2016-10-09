import urllib.request
import json
from Sensor import WioSensorReader, SensorDbWriter
from time import sleep, strftime, gmtime, time
from Database import Mongo

import ProtoConfig

sleep_time_sec = 10 # * 60 # 1 min

def run():
  sensor_db = Mongo.GetClient()

  wioConfig = ProtoConfig.getConfig()
  wioKairi = wioConfig.wioLinks[0]
  wioHavok = wioConfig.wioLinks[1]
  arduinoConfig = wioConfig.arduinos[0]

  air_quality = SensorReader(wioKairi, 'GroveAirqualityA0/quality')
  lux = WioSensorReader( wioHavok, 'GroveDigitalLightI2C0/lux')
  sound = WioSensorReader( wioHavok, 'GroveLoudnessA0/loudness')
  arduino = ArduinoSensorReader(arduinoConfig)
  clients = [SensorDbWriter(air_quality, sensor_db.air_quality),
             SensorDbWriter(lux, sensor_db.lux),
             SensorDbWriter(sound, sensor_db.loudness),
            ]

  while True:
    start = time()
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    for client in clients:
      client.GetAndInsert(date=date)
    end = time()
    delta = round(end - start, 0)
    print("Function took %ds" % delta)
    sleep_time_remain_sec = max(sleep_time_sec - delta, 0)
    print('Added data from %s sensors going to sleep for %ds (%dm)\n' % (
      len(clients), sleep_time_remain_sec, sleep_time_remain_sec/60))
    sleep(sleep_time_remain_sec) 

if __name__ == '__main__':
  run()

