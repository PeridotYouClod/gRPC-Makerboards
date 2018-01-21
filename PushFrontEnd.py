import concurrent.futures as futures
import grpc
import time

import ProtoConfig
import generated.proto_out.sensors_pb2 as sensors_pb2
import generated.proto_out.sensors_pb2_grpc as sensors_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class PushFrontEnd(sensors_grpc.PushFrontEndServicer):
  def __init__(self, protoConfig):
    super().__init__()
    pushchannel = grpc.insecure_channel('localhost:%s' % protoConfig.ports.pushPort)
    self.pushStub = sensors_grpc.PushStub(pushchannel)

  def Subscribe(self, request, context):
      status = "Subscribed" if request.status == 1 else "Unsubscribed"
      print('%s user %s' % (status, request.username))
      return self.pushStub.Subscribe(request)

  def StreamButtonPressed(self, request, context):
      for press in self.pushStub.StreamButtonPressed(
        sensors_pb2.GetButtonPressedRequest(index=request.index)):
          print('Passing on press event %s' % press)
          yield press

def serve():
  protoConfig = ProtoConfig.getConfig()
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  sensors_grpc.add_PushFrontEndServicer_to_server(PushFrontEnd(protoConfig), server)
  port = protoConfig.ports.pushFrontEndPort
  server.add_insecure_port('[::]:%s' % port)
  server.start()
  print('Started PushFrontEnd Server on Port %s ' % port)

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
