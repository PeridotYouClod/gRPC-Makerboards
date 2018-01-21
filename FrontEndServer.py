import concurrent.futures as futures
import grpc
import time

import ProtoConfig
import generated.proto_out.sensors_pb2 as sensors_pb2
import generated.proto_out.sensors_pb2_grpc as sensors_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class FrontEnd(sensors_grpc.FrontEndServicer):
  def __init__(self, protoConfig):
    super().__init__()
    wioChannel = grpc.insecure_channel('localhost:%s' % protoConfig.ports.wioPort)
    self.wioStub = sensors_grpc.WioLinkStub(wioChannel)
    arduinoChannel = grpc.insecure_channel('localhost:%s' % protoConfig.ports.arduinoPort)
    self.arduinoStub = sensors_grpc.ArduinoStub(arduinoChannel)

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

  def SendToRfBlaster(self, req, context):
    print('SendToRfBlaster')
    blasterRequest = sensors_pb2.SendToRfBlasterRequest(
      button=req.button,
      on=req.on
    )
    print("blasterRequest: %s" % blasterRequest)
    return self.arduinoStub.SendToRfBlaster(blasterRequest)


def serve():
  protoConfig = ProtoConfig.getConfig()
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_grpc.add_FrontEndServicer_to_server(FrontEnd(protoConfig), server)
  port = protoConfig.ports.frontEndPort
  server.add_insecure_port('[::]:%s' % port)
  server.start()
  print('Started FrontEnd Server on Port %s ' % port)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
