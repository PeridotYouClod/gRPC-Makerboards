import grpc
import proto_out.sensors_pb2 as sensors_pb2

def getLux(stub):
  req = sensors_pb2.GetLuxRequest()
  response = stub.GetLux(req)
  return response.lux

def getTemperature(stub):
  req = sensors_pb2.GetTemperatureRequest()
  response = stub.GetTemperature(req)
  return (response.temperature_c, round(response.temperature_f,1))

def getIrButtonPressed(stub):
  req = sensors_pb2.GetIrButtonPressedRequest()
  res1 = stub.GetIrButtonPressed(req)
  req = sensors_pb2.GetSonarRequest()
  res2 = stub.GetSonar(req)
  return (res1.button, res2)

def getSound(stub):
  req = sensors_pb2.GetSoundRequest()
  response = stub.GetSound(req)
  return response.loudness

def getSonar(stub):
  req = sensors_pb2.GetSonarRequest()
  response = stub.GetSonar(req)
  return response.distance

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = sensors_pb2.SensorsStub(channel)

  lux = getLux(stub)
  print('lux: ', lux)

  temperature = getTemperature(stub)
  print('temperature: ', temperature)

  irButton = getIrButtonPressed(stub)
  print('irButton: ', irButton)

  loudness = getSound(stub)
  print('loudness: ', loudness)

  req = sensors_pb2.GetButtonPressedRequest()
  buttonPressed = stub.GetButtonPressed(req).pressed
  print("buttonPressed", buttonPressed)
  req = sensors_pb2.SetLedStripRequest(
    length= 30,
    brightness=100 if buttonPressed else 0,
    speed=5)
  response = stub.SetLedStrip(req)


if __name__ == '__main__':
  run()
