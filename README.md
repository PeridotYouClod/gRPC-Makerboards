# gRPC Makerboards

## Runable Files
* Reader - Reads the values from the Sensor and stores them to a Mongo Database.
* Graph - Reads the values from the Mongo Database and Graphs it.
* WioServer - Sensor gRPC Server impleneted in Python.
* WioClient - Simple Sensor gRPC Client impleneted in Python.

## Build the Protobufs
    python -m grpc.tools.protoc \
      ./protos/sensors.proto ./protos/config.proto \
      --proto_path=./protos \
      --python_out=./proto_out \
      --grpc_python_out=./proto_out \
