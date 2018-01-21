import grpc
import generated.proto_out.sensors_pb2_grpc as sensors_grpc
import generated.proto_out.sensors_pb2 as sensors_pb2
import generated.proto_out.dao_pb2_grpc as dao_pb2
from time import sleep
import ProtoConfig

def run():
  protoConfig = ProtoConfig.getConfig()
  channel = grpc.insecure_channel('localhost:%s' % protoConfig.ports.frontEndPort)
  stub = sensors_grpc.FrontEndStub(channel)
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
