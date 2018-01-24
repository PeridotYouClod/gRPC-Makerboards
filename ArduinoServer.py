import concurrent.futures as futures
import grpc
import time

import ProtoConfig
import generated.proto_out.sensors_pb2 as sensors_pb2
import generated.proto_out.sensors_pb2_grpc as sensors_grpc
from pylibs.Sensor import ArduinoSensorReader

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Arduino(sensors_grpc.ArduinoServicer):
  def __init__(self, arduinos):
    super().__init__()
    # TODO: Add registration for different methods in config file rather than this hack
    arduinoDevices = [ArduinoSensorReader(arduino) for arduino in arduinos]
    self.deviceMap = {
      "GetIrButtonPressed" : arduinoDevices[0],
      "GetSonar" :  arduinoDevices[0],
      "SendToRfBlaster" : arduinoDevices[1],
    }

  def GetIrButtonPressed(self, request, context):
    device = self.deviceMap["GetIrButtonPressed"]
    clean_value = device.GetCurrentValue()
    print('Returning Button Press: %s' % clean_value)
    return sensors_pb2.GetIrButtonPressedReply(button=clean_value)

  def GetSonar(self, request, context):
    device = self.deviceMap["GetSonar"]
    clean_value = device.GetCurrentValue()
    print('Returning Sonar: %s' % clean_value)
    return sensors_pb2.GetSonarReply(distance=clean_value)

  def SendToRfBlaster(self, request, context):
    print("Sending RF Blaster Button Press: %s" % request)
    device = self.deviceMap["SendToRfBlaster"]
    device.sendRfBlast(request.button, request.on)
    return sensors_pb2.SendToRfBlasterReply(success=True)


def serve():
  protoConfig = ProtoConfig.getConfig()
  arduinos = protoConfig.arduinos

  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_grpc.add_ArduinoServicer_to_server(Arduino(arduinos), server)
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
