import concurrent.futures as futures
import time
import grpc
import serial
import re
import sys

import ProtoConfig
from Sensor import WioSensorReader
import proto_out.sensors_pb2 as sensors_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
PORT = 50050

class FrontEnd(sensors_pb2.FrontEndServicer):
  def __init__(self):
    super().__init__()
    wioChannel = grpc.insecure_channel('localhost:50051')
    self.wioStub = sensors_pb2.WioLinkStub(wioChannel)
    channel = grpc.insecure_channel('localhost:50052')
    self.arduinoStub = sensors_pb2.ArduinoStub(channel)


  def GetIrButtonPressed(self, request, context):
    print('GetIrButtonPressed')
    return self.arduinoStub.GetIrButtonPressed(
      sensors_pb2.GetIrButtonPressedRequest())

  def GetSonar(self, request, context):
    print('GetSonar')
    return self.arduinoStub.GetSonar(sensors_pb2.GetSonarRequest())

  def GetLux(self, request, context):
    print('GetLux')
    return self.wioStub.GetLux(sensors_pb2.GetLuxRequest())

  def GetTemperature(self, request, context):
    print('GetTemperature')
    return self.wioStub.GetTemperature(sensors_pb2.GetTemperatureRequest())

  def GetSound(self, request, context):
    print('GetSound')
    return self.wioStub.GetSound(sensors_pb2.GetSoundRequest())

  def SetLedStrip(self, req, context):
    print('SetLedStrip')
    return self.wioStub.SetLedStrip(sensors_pb2.SetLedStripRequest())

  def GetButtonPressed(self, req, context):
    print('GetButtonPressed')
    return self.wioStub.GetButtonPressed(sensors_pb2.GetButtonPressedRequest())

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_pb2.add_FrontEndServicer_to_server(FrontEnd(), server)
  server.add_insecure_port('[::]:%s' % PORT)
  print('Starting Server...')
  server.start()
  print('Server Started on Port %s' % PORT)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
