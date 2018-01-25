import json
import grpc

import generated.proto_out.sensors_pb2 as sensors_pb2
import generated.proto_out.sensors_pb2_grpc as sensors_grpc
import ProtoConfig

from google.cloud import pubsub

PUSH_BUTTON_TOPIC = 'projects/wiolink-1337/topics/push-button'
PUSH_BUTTON_SUBSCRIPTION = 'projects/wiolink-1337/subscriptions/local-sub'


def run():
  protoConfig = ProtoConfig.getConfig()
  channel = grpc.insecure_channel('localhost:%s' % protoConfig.ports.frontEndPort)
  stub = sensors_grpc.FrontEndStub(channel)

  subscriber = pubsub.SubscriberClient()
  subscription = subscriber.subscribe(PUSH_BUTTON_SUBSCRIPTION)

  def gotMessage(message):
      print('message.data: %s' % message.data)
      messageJson = json.loads(message.data)
      request = sensors_pb2.SendToRfBlasterRequest(
        button=int(messageJson['button-destination']),
        on=(messageJson['button-state'] == 'on')
      )
      stub.SendToRfBlaster(request)
      message.ack()

  messageFuture = subscription.open(gotMessage)

  while True:
    print('Waiting for new message...')
    try:
        messageFuture.result()
    except Exception as ex:
        print('Error handling message: %s' % ex)


if __name__ == '__main__':
  run()
