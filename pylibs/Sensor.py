import json
import serial
import urllib.request

class WioSensorReader(object):
  def __init__(self, wioConfig, groveName):
    self.wioConfig = wioConfig
    self.groveConfig = wioConfig.sensors[groveName]

  def getName(self):
    return self.groveConfig

  def _accessTokenUrl(self):
      return '?access_token=%s' % self.wioConfig.accessToken

  def getUrl(self):
      return (self.wioConfig.rootUrl + self.groveConfig.apiMethod
        + self._accessTokenUrl())

  def GetCurrentValue(self):
      try:
        print(self.getUrl())
        request = urllib.request.urlopen(self.getUrl())
        return_val = request.read().decode('utf-8')
        request.close()
        return json.loads(return_val)
      except:
        return None

  def setUrl(self, urlArgsStr):
      url = (self.wioConfig.rootUrl + self.groveConfig.apiMethod
             + urlArgsStr + self._accessTokenUrl())
      print('setUrl: ', url)
      params = urllib.parse.urlencode({}).encode('utf-8')
      urllib.request.urlopen(url, data=params)

  def printRequest(self):
      print(self.GetCurrentValue())

class ArduinoSensorReader(object):
  def __init__(self, arduinoConfig):
    self.config = arduinoConfig
    self.serial = serial.Serial(
      arduinoConfig.comPort, arduinoConfig.baudRate)

  def getName(self):
    return 'Arduino on %s' % arduinoConfig.comPort

  def GetCurrentValue(self):
    serial_value = self.serial.readline()
    print('Got Arduino Value: %s' % serial_value)
    try:
        clean_value = int(serial_value)
    except ValueError as e:
        print("Got value error %s returning 0" % e)
        clean_value = 0
    self.serial.reset_input_buffer()
    return clean_value

  def sendRfBlast(self, button, on):
    opcode = "%s%s" % (bin(button)[2:], bin(on)[2:])
    self.serial.write(opcode.encode())


class SensorDbWriter(object):
  def __init__(self, sensor, db_col):
    print('sensor: %s\ndb_col: %s' % (sensor, db_col))
    self.sensor = sensor
    self.db_col = db_col

  def insert(self, date):
    current_val = self.sensor.GetCurrentValue()
    if current_val:
      current_val['date'] = date
      print('Inserting: %s' % current_val)
      self.db_col.insert_one(current_val)
    else:
      print('Faied to get value for %s' % self.sensor.getName())
    return current_val
