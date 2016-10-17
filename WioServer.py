import concurrent.futures as futures
import time
import grpc

import ProtoConfig
import generated.proto_out.sensors_pb2 as sensors_pb2
from pylibs.Sensor import WioSensorReader

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class WioLink(sensors_pb2.WioLinkServicer):
  def __init__(self, protoConfig):
    super().__init__()

    wioHavok = protoConfig.wioLinks['havok']
    wioKairi = protoConfig.wioLinks['kairi']
    self.temperature_c = WioSensorReader(wioHavok, 'temperature_c')
    self.lux = WioSensorReader(wioHavok, 'lux')
    self.sound = WioSensorReader(wioHavok, 'loudness')
    self.ledStrip = WioSensorReader(wioHavok, 'ledStrip')
    self.button = WioSensorReader(wioHavok, 'button')

  def GetLux(self, request, context):
    lux = self.lux.GetCurrentValue()
    print('Returning Brigtness: %s' % lux)
    return sensors_pb2.GetLuxReply(lux=lux['lux'])

  def GetTemperature(self, request, context):
    temperature_c = self.temperature_c.GetCurrentValue()['celsius_degree']
    temperature_f = float(temperature_c) * (9./5.) + 32.
    print('Returning Temperature: %s*c / %s*f' %
      (temperature_c, temperature_f))
    return sensors_pb2.GetTemperatureReply(
      temperature_c=temperature_c,
      temperature_f=temperature_f)

  def GetSound(self, request, context):
    sound = self.sound.GetCurrentValue()
    print('Returning Loudness: %s' % sound)
    return sensors_pb2.GetSoundReply(loudness=sound['loudness'])

  def SetLedStrip(self, req, context):
    url = '/%s/%s/%s' % (req.length, req.brightness, req.speed)
    self.ledStrip.setUrl(url)
    return sensors_pb2.SetLedStripReply()

  def GetButtonPressed(self, req, context):
    pressedVal = self.button.GetCurrentValue()
    pressed = pressedVal['pressed']
    print('Returning Pressed: %s' % pressedVal)
    val = True if pressed == 1 else False
    print('Returning Pressed: %s' % val)
    return sensors_pb2.GetButtonPressedReply(pressed=val)

def serve():
  protoConfig = ProtoConfig.getConfig()
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_pb2.add_WioLinkServicer_to_server(WioLink(protoConfig), server)
  port = protoConfig.ports.wioPort
  server.add_insecure_port('[::]:%s' % port)
  server.start()
  print('Started Wio Server on Port %s ' % port)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
