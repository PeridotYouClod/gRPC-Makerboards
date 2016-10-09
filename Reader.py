import json
from time import sleep, strftime, gmtime, time
import urllib.request

from Database import Mongo
import ProtoConfig
from Sensor import WioSensorReader, SensorDbWriter

sleep_time_sec = 10

def run():
  sensor_db = Mongo().GetClient()
  protoConfig = ProtoConfig.getConfig()

  wioHavok = protoConfig.wioLinks['havok']
  sensor_lux = WioSensorReader(wioHavok, 'lux')
  sensor_loudness = WioSensorReader(wioHavok, 'loudness')
  sensor_temperature_c = WioSensorReader(wioHavok, 'temperature_c')

  wioKairi = protoConfig.wioLinks['kairi']
  sensor_airquality = WioSensorReader(wioKairi, 'airquality')
  sensor_barometer = WioSensorReader(wioKairi, 'barometer')
  sensor_shaked = WioSensorReader(wioKairi, 'shaked')

  clients = [
    SensorDbWriter(sensor_temperature_c, sensor_db.temperature_c),
    SensorDbWriter(sensor_lux, sensor_db.lux),
    SensorDbWriter(sensor_loudness, sensor_db.loudness),
    SensorDbWriter(sensor_airquality, sensor_db.airquality),
    SensorDbWriter(sensor_barometer, sensor_db.barometer),
    SensorDbWriter(sensor_shaked, sensor_db.shaked),
  ]

  while True:
    start = time()
    date = strftime('%Y-%m-%d %H:%M:%S', gmtime())
    for client in clients:
      client.insert(date=date)
    end = time()
    delta = round(end - start, 0)
    print('Function took %ds' % delta)
    sleep_time_remain_sec = max(sleep_time_sec - delta, 0)
    print('Added data from %s sensors going to sleep for %ds (%dm)\n' % (
      len(clients), sleep_time_remain_sec, sleep_time_remain_sec/60))
    sleep(sleep_time_remain_sec)

if __name__ == '__main__':
  run()
