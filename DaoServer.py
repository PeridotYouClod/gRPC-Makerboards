from concurrent import futures
import time
import Reader
import grpc
import re
import sys

from Database import Mongo
import proto_out.sensors_pb2 as sensors_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
PORT = 50049

class Dao(sensors_pb2.DaoServicer):
  def __init__(self):
    super().__init__()
    self.sensor_db = Mongo()
    # initalized Db
    self.sensor_db.GetClient()

  def Select(self, request, context):
    table = request.table
    limit = request.limit
    cols = request.cols
    print('Got request {\n%s}\n' % (request))
    colNames = [col.name for col in cols]
    findResult = self.sensor_db.Find(table=table, columns=colNames, limit=limit)
    allColValues = {} # Col name to list of vals
    for col in cols:
        allColValues[col.name] = {'colType': col.coltype, 'values': []}
    for doc in findResult:
        for col in cols:
            # print('%s added to %s' % (doc[col.name], col.name))
            allColValues[col.name]['values'].append(doc[col.name])
    dataColumns = []
    for (colName, colValues) in allColValues.items():
        colType = colValues['colType']
        vals = colValues['values']
        # print("colName: %s, coltype: %s, colValues: %s" %
        #   (colName, colType, vals))
        if colType == sensors_pb2.RequestCol.INT:
            dataColumn = sensors_pb2.DataColumn(name=colName, intValues=vals)
        elif colType == sensors_pb2.RequestCol.STRING:
            dataColumn = sensors_pb2.DataColumn(name=colName, stringValues=vals)
        else:
            print("ERROR UNKNOWN TYPE")
        dataColumns.append(dataColumn)
    return sensors_pb2.SelectReply(columns=dataColumns)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_pb2.add_DaoServicer_to_server(Dao(), server)
  server.add_insecure_port('[::]:%s' % PORT)
  server.start()
  print('Server Started on Port %s ' % PORT)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
