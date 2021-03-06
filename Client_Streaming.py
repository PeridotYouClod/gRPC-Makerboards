import grpc
import time
import generated.proto_out.sensors_pb2_grpc as sensors_grpc
import generated.proto_out.sensors_pb2 as sensors_pb2
import ProtoConfig

def run():
  protoConfig = ProtoConfig.getConfig()
  channel = grpc.insecure_channel('localhost:%s' % protoConfig.ports.pushFrontEndPort)
  stub = sensors_grpc.PushFrontEndStub(channel)

  subscribeRequest = sensors_pb2.SubscribeRequest(
    status=sensors_pb2.SubscribeRequest.SUBSCRIBE,
    username="peridot"
  )
  subscribeReply = stub.Subscribe(subscribeRequest)
  start_index = subscribeReply.start_index or 0
  print(subscribeReply)
  req = sensors_pb2.GetButtonPressedRequest(
    index=subscribeReply.start_index)
  while True:
    for event in stub.StreamButtonPressed(req):
      req.index += 1
      print('index: %s, event: %s' % (req.index, event))
    time.sleep(1)

if __name__ == '__main__':
  run()
