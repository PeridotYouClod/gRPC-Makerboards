==Build the Protobufs==
    python -m grpc.tools.protoc \
      ./protos/sensors.proto ./protos/config.proto \
      --proto_path=./protos \
      --python_out=./proto_out \
      --grpc_python_out=./proto_out \
