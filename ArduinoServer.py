import concurrent.futures as futures
import grpc
import time

import ProtoConfig
import generated.proto_out.sensors_pb2 as sensors_pb2
from pylibs.Sensor import ArduinoSensorReader

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
PORT = 50052

class Arduino(sensors_pb2.ArduinoServicer):
  def __init__(self):
    super().__init__()
    protoConfig = ProtoConfig.getConfig()
    arduino = protoConfig.arduinos[0]
    self.sensorReader = ArduinoSensorReader(arduino)

  def GetIrButtonPressed(self, request, context):
    clean_value = self.sensorReader.GetCurrentValue()
    print('Returning Button Press: %s' % clean_value)
    return sensors_pb2.GetIrButtonPressedReply(button=clean_value)

  def GetSonar(self, request, context):
    clean_value = self.sensorReader.GetCurrentValue()
    print('Returning Sonar: %s' % clean_value)
    return sensors_pb2.GetSonarReply(distance=clean_value)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_pb2.add_ArduinoServicer_to_server(Arduino(), server)
  server.add_insecure_port('[::]:%s' % PORT)
  server.start()
  print('Started Arduino Server on Port %s ' % PORT)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
