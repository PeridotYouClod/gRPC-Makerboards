import concurrent.futures as futures
import grpc
import time

import ProtoConfig
import generated.proto_out.sensors_pb2 as sensors_pb2
from pylibs.Sensor import ArduinoSensorReader

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Arduino(sensors_pb2.ArduinoServicer):
  def __init__(self, arduino):
    super().__init__()
    self.sensorReader = ArduinoSensorReader(arduino)

  def GetIrButtonPressed(self, request, context):
    clean_value = self.sensorReader.GetCurrentValue()
    print('Returning Button Press: %s' % clean_value)
    return sensors_pb2.GetIrButtonPressedReply(button=clean_value)

  def GetSonar(self, request, context):
    clean_value = self.sensorReader.GetCurrentValue()
    print('Returning Sonar: %s' % clean_value)
    return sensors_pb2.GetSonarReply(distance=clean_value)

  def SendToRfBlaster(self, request, context):
    print("Sending RF Blaster Button Press: %s" % request)
    self.sensorReader.sendRfBlast(request.button,request.on)
    return sensors_pb2.SendToRfBlasterReply(success=True)


def serve():
  protoConfig = ProtoConfig.getConfig()
  arduino = protoConfig.arduinos[0]

  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_pb2.add_ArduinoServicer_to_server(Arduino(arduino), server)
  port = protoConfig.ports.arduinoPort
  server.add_insecure_port('[::]:%s' % port)
  server.start()
  print('Started Arduino Server on Port %s ' % port)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
