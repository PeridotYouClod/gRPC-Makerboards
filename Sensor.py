import urllib.request
import json

class WioSensorReader(object):
  def __init__(self, wioConfig, groveConfig):
    self.wioConfig = wioConfig
    self.groveConfig = groveConfig

  def getName(self):
    return self.groveConfig

  def getUrl(self):
      return (self.wioConfig.rootUrl + self.groveConfig.apiMethod
        + self.wioConfig.apiKey)

  def GetCurrentValue(self):
      try:
        request = urllib.request.urlopen(self.getUrl())
        return_val = request.read().decode("utf-8")
        request.close()
        return json.loads(return_val)
      except:
        return None

  def postRequest(self, obj):
      pass

  def printRequest(self):
      print(self.GetCurrentValue())

class ArduinoSensorReader(object):
  def __init__(self, arduinoConfig):
    self.config = arduinoConfig
    self.serial = serial.Serial(arduinoConfig.comPort, arduinoConfig.baudRate)

  def getName(self):
    return "Arduino on %s" % arduinoConfig.comPort

  def GetCurrentValue(self):
    serial_value = self.ser.readline()
    clean_value = int(serial_value)
    self.ser.reset_input_buffer()
    print("Returning Arduino Value: %s" % clean_value)
    return clean_value

class SensorDbWriter(object):
  def __init__(self, sensor, db_col):
    print("sensor: %s\ndb_col: %s" % (sensor, db_col))
    self.sensor = sensor
    self.db_col = db_col

  def insert(self, date):
    current_val = self.sensor.GetCurrentValue()
    if current_val:
      current_val['date'] = date
      print("Inserting: %s" % current_val)
      self.db_col.insert_one(current_val)
    else:
      print("Faied to get value for %s" % self.sensor.getName())
    return current_val
