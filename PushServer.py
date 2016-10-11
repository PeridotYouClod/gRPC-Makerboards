import concurrent.futures as futures
import grpc
import re
import sys
import time
import websocket

import ProtoConfig
import proto_out.sensors_pb2 as sensors_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
PORT = 50090

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

  def SubscribeButtonPressed(self, request, context):
    if request.update.status == sensors_pb2.SubscriptionUpdate.SUBSCRIBE:
      start_index = len(self.pressEvents)
      print('User %s subscribed at index %s' %
            (request.username, start_index))
      yield sensors_pb2.GetButtonPressedReply(start_index=start_index)
    else:
      for pressEvent in self.pressEvents[request.index:]:
        yield pressEvent

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  protoConfig = ProtoConfig.getConfig()
  pushServer = Push(accessToken=protoConfig.wioLinks['havok'].accessToken)
  sensors_pb2.add_PushServicer_to_server(pushServer, server)
  server.add_insecure_port('[::]:%s' % PORT)
  server.start()
  print('Server Started on Port %s ' % PORT)

  try:
    while True:
      websocket.enableTrace(True)
      ws = websocket.WebSocketApp(
        "wss://us.wio.seeed.io/v1/node/event",
        on_message = pushServer.on_message,
        on_error = pushServer.on_error,
        on_close = pushServer.on_close)
      ws.on_open = pushServer.on_open
      ws.run_forever()
  except KeyboardInterrupt:
    server.stop(0)


if __name__ == '__main__':
  serve()
