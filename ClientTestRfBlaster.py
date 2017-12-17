import grpc
import generated.proto_out.sensors_pb2 as sensors_pb2
import generated.proto_out.dao_pb2 as dao_pb2
from time import sleep

def run():
  channel = grpc.insecure_channel('localhost:50050')
  stub = sensors_pb2.FrontEndStub(channel)
  rfBlasterRequestOn = sensors_pb2.SendToRfBlasterRequest(
      button=2,
      on=True
  )
  rfBlasterRequestOff = sensors_pb2.SendToRfBlasterRequest(
      button=2,
      on=False
  )
  stub.SendToRfBlaster(rfBlasterRequestOn)
  sleep(1)
  stub.SendToRfBlaster(rfBlasterRequestOff)
  exit()
if __name__ == '__main__':
  run()
