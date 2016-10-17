import concurrent.futures as futures
import grpc
import time
import websocket

import ProtoConfig
import generated.proto_out.sensors_pb2 as sensors_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Push(sensors_pb2.PushServicer):
  def __init__(self, accessToken):
    super().__init__()
    self.accessToken = accessToken
    self.pressEvents = []

  def on_message(self, ws, message):
    print(message)
    reply = sensors_pb2.GetButtonPressedReply(pressed=True)
    self.pressEvents.append(reply)

  def on_error(self, ws, error):
    print(error)

  def on_close(self, ws):
    print("### closed ###")

  def on_open(self, ws):
    print("Opening and sending token %s" % self.accessToken)
    ws.send(self.accessToken);

  def Subscribe(self, request, context):
    start_index = len(self.pressEvents)
    print('request %s' % request)
    if request.status == sensors_pb2.SubscribeRequest.SUBSCRIBE:
      print('User %s subscribed at index %s' % (request.username, start_index))
    elif request.status == sensors_pb2.SubscribeRequest.UNSUBSCRIBE:
      print('User %s unsubscribed at index %s' %
        (request.username, start_index))
    else:
      print('nop')
    return sensors_pb2.SubscribeReply(start_index=start_index)

  def StreamButtonPressed(self, request, context):
    for pressEvent in self.pressEvents[request.index:]:
      yield pressEvent

def serve():
  protoConfig = ProtoConfig.getConfig()
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  pushServer = Push(accessToken=protoConfig.wioLinks['havok'].accessToken)
  sensors_pb2.add_PushServicer_to_server(pushServer, server)
  port = protoConfig.ports.pushPort
  server.add_insecure_port('[::]:%s' % port)
  server.start()
  print('Started Push Server on Port %s ' % port)

  websocket.enableTrace(True)
  ws = websocket.WebSocketApp(
    "wss://us.wio.seeed.io/v1/node/event",
    on_message = pushServer.on_message,
    on_error = pushServer.on_error,
    on_close = pushServer.on_close)
  ws.on_open = pushServer.on_open
  ws.run_forever()

  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
