# gRPC Makerboards

## Runnable Files
### Servers (Implemented in Python however gRPC allows any language implemtation)
* WioServer.py - gRPC Server connecting to a [Wio Link](http://wiki.seeed.cc/Wio_Link/) via REST.
* ArduinoServer.py - gRPC Server connecting to an [Arduino](https://www.arduino.cc/en/Guide/Introduction) via COM port.
* FrontEndServer.py - gRPC Server communicates to backend servers to give a single connection point to the client.
* Client.py - Simple gRPC Client example.

### Automatic Database Storage
* Reader - Reads the values from the Sensor and stores them to a Mongo Database.

### Visualization
* Graph - Reads the values from the Mongo Database and Graphs it.

## Set Up Environment

    sudo apt-get install git

    # Install mongo and set up database folder
    sudo apt-get install mongodb
    sudo mkdir /data/db
    sudo chown <YOUR USERNAME> -R /data/

    # Install python3 pip if it is missing
    sudo apt-get install python3-pip
    pip3 install --upgrade pip

    # Grab gRPC for protobufs and servers
    sudo pip3 install grpcio
    sudo pip3 install grpcio-tools

    # Get required python libs
    pip3 install pymongo
    pip3 install urllib3
    pip3 install plotly

## Build the Protobufs
 Every time a .proto file is changed run this script to create new implementations of the edited protobuf or gRPC Server.
 
    python -m grpc.tools.protoc \
      ./protos/sensors.proto ./protos/config.proto \
      --proto_path=./protos \
      --python_out=./proto_out \
      --grpc_python_out=./proto_out \
