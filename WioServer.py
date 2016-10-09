from concurrent import futures
import time
import Reader
import grpc
from Sensor import WioSensorReader
import ProtoConfig
import serial
import re
import sys

import proto_out.sensors_pb2 as sensors_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Sensors(sensors_pb2.SensorsServicer):
  def __init__(self):
    super().__init__()
    protoConfig = ProtoConfig.getConfig()

    wioHavok = protoConfig.wioLinks['havok']
    self.temperature_c = WioSensorReader(wioHavok, 'temperature_c')
    self.lux = WioSensorReader(wioHavok, 'lux')
    self.sound = WioSensorReader(wioHavok, 'loudness')
    self.ledStrip = WioSensorReader(wioHavok, 'ledStrip')
    self.button = WioSensorReader(wioHavok, 'button')

    arduino = protoConfig.arduinos[0]
    self.ser = serial.Serial(arduino.comPort, arduino.baudRate)

  def GetLux(self, request, context):
    lux = self.lux.GetCurrentValue()
    print("Returning Brigtness: %s" % lux)
    return sensors_pb2.GetLuxReply(lux=lux['lux'])

  def GetTemperature(self, request, context):
    temperature_c = self.temperature_c.['temperature_c']
    temperature_f = float(temperature_c) * (9./5.) + 32.
    print("Returning Temperature: %s*c / %s*f" %
      (temperature_c, temperature_f))
    return sensors_pb2.GetTemperatureReply(
      temperature_c=temperature_c,
      temperature_f=temperature_f)

  def GetSound(self, request, context):
    sound = self.sound.GetCurrentValue()
    print("Returning Loudness: %s" % sound)
    return sensors_pb2.GetLoudnessReply(loudness=sound['loudness'])

  def GetIrButtonPressed(self, request, context):
    serial_value = self.ser.readline()
    clean_value = int(serial_value)
    print("Returning Button Press: %s" % clean_value)
    return sensors_pb2.GetIrButtonPressedReply(button=clean_value)

  def GetSonar(self, request, context):
    serial_value = self.ser.readline()
    clean_value = int(serial_value)
    self.ser.reset_input_buffer()
    print("Returning Sonar: %s" % clean_value)
    return sensors_pb2.GetSonarReply(distance=clean_value)

  def SetLedStrip(self, req, context):
    url = "/%s/%s/%s" % (req.length, req.brightness, req.speed)
    self.ledStrip.setUrl(url)
    return sensors_pb2.SetLedStripReply()

 def GetButtonPressed(self, req, context):
   pressedVal = self.button.GetCurrentValue()
   pressed = pressedVal['pressed']
   print("Returning Pressed: %s" % pressedVal)
   val = True if pressed == 1 else False
   print("Returning Pressed: %s" % val)
   return sensors_pb2.GetButtonPressedReply(pressed=val)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_pb2.add_SensorsServicer_to_server(Sensors(), server)
  server.add_insecure_port('[::]:50051')
  print('Starting Server on Port 50051')
  server.start()

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
