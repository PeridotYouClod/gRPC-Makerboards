import grpc
import time
import generated.proto_out.sensors_pb2 as sensors_pb2

def run():
  channel = grpc.insecure_channel('localhost:50090')
  stub = sensors_pb2.PushStub(channel)

  subscribeRequest = sensors_pb2.SubscribeButtonPressedRequest(
    update=sensors_pb2.SubscriptionUpdate(
      status=sensors_pb2.SubscriptionUpdate.SUBSCRIBE),
    username="peridot"
  )
  subscribeReply = stub.SubscribeButtonPressed(subscribeRequest).next()
  print(subscribeReply)
  req = sensors_pb2.SubscribeButtonPressedRequest(
    index=subscribeReply.start_index)
  while True:
    eventList = stub.SubscribeButtonPressed(req)
    for event in eventList:
      req.index += 1
      print('index: %s, event: %s' % (req.index, event))
    time.sleep(1)

if __name__ == '__main__':
  run()
