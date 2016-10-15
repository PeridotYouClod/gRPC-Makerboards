import concurrent.futures as futures
import grpc
import re
import sys
import time

from Database import Mongo
import Reader
import generated.proto_out.dao_pb2 as dao_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
PORT = 50040

class Dao(dao_pb2.DaoServicer):
  def __init__(self, sensor_db):
    super().__init__()
    self.sensor_db = sensor_db

  def Select(self, request, context):
    table = request.table
    limit = request.limit
    cols = request.cols
    print('Got request {\n%s}\n' % (request))
    colNames = [col.name for col in cols]
    findResult = self.sensor_db.Find(table=table, columns=colNames, limit=limit)
    allColValues = {col.name: [] for col in cols} # Col name to list of vals
    for doc in findResult:
        for col in cols:
            # print('%s added to %s' % (doc[col.name], col.name))
            allColValues[col.name].append(doc[col.name])
    dataColumns = [self._NewDataColumn(colName, vals) for (colName, vals)
                   in allColValues.items()]
    return dao_pb2.SelectReply(columns=dataColumns)

  def _NewDataColumn(self, columnName, values):
    datacolumn = dao_pb2.DataColumn(name=columnName)
    if not values:
        print("Warning: No values found.")
    elif type(values[0]) is int:
        datacolumn.intValues.extend(values)
    elif type(values[0]) is str:
        datacolumn.stringValues.extend(values)
    else:
        print("ERROR: Unknown Type!")
    return datacolumn


def serve():
  sensor_db = Mongo()
  sensor_db.GetClient() # initalize the Db
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  dao_pb2.add_DaoServicer_to_server(Dao(sensor_db), server)
  server.add_insecure_port('[::]:%s' % PORT)
  server.start()
  print('Started Dao Server on Port %s ' % PORT)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
