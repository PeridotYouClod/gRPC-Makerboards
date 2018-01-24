import concurrent.futures as futures
import grpc
import time

import ProtoConfig
import generated.proto_out.sensors_pb2 as sensors_pb2
import generated.proto_out.sensors_pb2_grpc as sensors_grpc
import generated.proto_out.config_pb2 as config_pb2

from pylibs.Sensor import ArduinoSensorReader

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Arduino(sensors_grpc.ArduinoServicer):
  def __init__(self, arduinos):
    super().__init__()
    arduinoDevices = [ArduinoSensorReader(arduino) for arduino in arduinos]
    self.deviceMap = dict([self._DeviceForFunction(func[1], func[0], arduinoDevices) for
     func in config_pb2.ArduinoFunction.items()[1:]]) # Skip UNKNOWN

  def _DeviceForFunction(self, func, funcName, devices):
    devicesWithFunction = [device for device in devices if func in device.functions]
    if(len(devicesWithFunction) == 0):
      print('%s not handled by server' % funcName)
      return (func, None)
    returnDevice = devicesWithFunction[0]
    if(len(devicesWithFunction) > 1):
      print('%s handled by more than one device, %s will be used' % (funcName, returnDevice))
    return (func, returnDevice)

  def GetIrButtonPressed(self, request, context):
    device = self.deviceMap[config_pb2.GET_IR_BUTTON_PRESSED]
    clean_value = device.GetCurrentValue()
    print('Returning Button Press: %s' % clean_value)
    return sensors_pb2.GetIrButtonPressedReply(button=clean_value)

  def GetSonar(self, request, context):
    device = self.deviceMap[config_pb2.GET_SONAR]
    clean_value = device.GetCurrentValue()
    print('Returning Sonar: %s' % clean_value)
    return sensors_pb2.GetSonarReply(distance=clean_value)

  def SendToRfBlaster(self, request, context):
    print("Sending RF Blaster Button Press: %s" % request)
    device = self.deviceMap[config_pb2.SEND_RF_REMOTE]
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
