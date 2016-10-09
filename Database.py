from pymongo import MongoClient

class Mongo(object):

  def __init__(self, port=27017):
    self.db = None
    self.port = port

  def GetClient(self):
    if self.db is None:
      print('Connecting to database mongodb://127.0.0.1:%s' % self.port)
      # NOTE! This is the tabele you connect to!
      self.db = MongoClient('mongodb://127.0.0.1:%s' % self.port).Sensor # <-- Here
    else:
      print('Reusing Connection!')
    return self.db

  def Find(self, col, limit=None):
    if limit:
      return self.db[col].find().sort('date', -1).limit(limit)
    return self.db[col].find().sort('date', -1)
