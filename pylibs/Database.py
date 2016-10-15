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

  def Find(self, table, limit=0, columns=None):
      cols = columns or []
      projection = {'_id': 0} # _id defaults to 1 so it is supressed.
      for col in cols:
          projection[col] = 1
      return self.db[table].find({},projection).sort('date', -1).limit(limit)
