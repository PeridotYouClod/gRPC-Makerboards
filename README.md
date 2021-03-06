## Runnable Files

### gRPC Servers (Implemented in Python however gRPC allows any language implemtation)
* WioServer.py - Connects to one or more [Wio Links](http://wiki.seeed.cc/Wio_Link/) via REST.
* ArduinoServer.py - Connects to one or more  [Arduinos](https://www.arduino.cc/en/Guide/Introduction) via COM port.
* FrontEndServer.py - Communicates to backend servers to give a single connection point to the client.
* PushFrontEnd.py - Communicates to backend servers to give a single connection point to the client for streaming requests.
* DaoServer.py - Communicate with the database.
* PushServer.py - Receive push events from devices.

### Clients
* Client.py - Simple gRPC Client example.
* Client_Streaming.py - Streaming gRPC Client example.

### Automatic Database Storage
* Reader.py - Reads the values from the Sensor and stores them to a Mongo Database.

### Visualization
* Graph.py - Reads the values from the Mongo Database and Graphs it.

### Protobuf Files
* config.proto - Defines how the config file should be created.  
* sensors.proto - Defines each of the Servers and all of the messages to the sensors. (TODO: too much currenty, break it up)
* dao.proto - Defines the Dao Server and the query and reply fo database interactions.

## Set Up Environment

### Linux
    sudo apt-get install git

    # Install mongo and set up database folder
    sudo apt-get install mongodb
    sudo mkdir -p /data/db
    sudo chown $USER -R /data/

    # Install python3 pip if it is missing
    sudo apt-get install python3-pip
    pip3 install --upgrade pip

    # Install requirements
    pip3 install -r requirements.txt --user

#### Raspberry Pi Potential Issues
    # Make sure the clock is correct if it is wrong run
    sudo raspi-config
    # Select Internationalisation Options
    # Select I2 Change Timezone
    # Select Finish

    # Getting CERTIFICATE_VERIFY_FAILED?
    sudo apt-get update
    sudo apt-get install libssl-dev
    sudo pip3 install libffi-dev # OR next line
    sudo apt-get install libffi-dev
    pip3 install cryptography

### Mac
    brew install git

    # Install mongo and set up database folder
    brew install mongodb
    sudo mkdir -p /data/db
    sudo chown $USER -R /data/

    # Install python3 pip if it is missing
    brew install python3
    pip3 install --upgrade pip

    # Install requirements
    pip3 install -r requirements.txt --user

## Set up your ProtoConfig.py file
Copy the ProtoConfigExample.py to ProtoConfig.py

    mv ProtoConfigExample.py ProtoConfig.py

Fill in your ProtoConfig.py with the instructions in the file. For help see [WioLink Help](https://github.com/sorahavok/gRpc-Hardware/edit/master/README.md#WioLink-Help) and [Arduino Help](https://github.com/sorahavok/gRpc-Hardware/edit/master/README.md#Arduino-Help)

## Build the Protobufs
Every time a .proto file is changed run this script to create new implementations of the edited protobuf or gRPC Server.

Linux:

    python3 -m grpc.tools.protoc \
      ./proto/*.proto \
      --proto_path=./proto/ \
      --python_out=./generated/proto_out \
      --grpc_python_out=./generated/proto_out

Mac:

    python3 -m grpc.tools.protoc ./proto/*.proto --proto_path=./proto/  --python_out=./generated/proto_out  --grpc_python_out=./generated/proto_out

## How Do I Run Everything?
The basic procedure is launch all the servers then run a Client

### Production
If you have a working version and don't need debug messages use this

    python3 WioServer.py &
    python3 ArduinoServer.py &
    python3 DaoServer.py &
    python3 FrontEndServer.py &
    python3 PushServer.py &
    python3 Client.py

### Debug
While developing it is useful to have all the different servers in different terminals

    python3 WioServer.py
    python3 ArduinoServer.py
    python3 DaoServer.py
    python3 FrontEndServer.py
    python3 PushServer.py
    python3 Client.py

### How do I kill PushServer.py?
PushServer is a bit odd right now, it is a gRPC server and a websocket in the same server and both need to be killed so [Ctrl][c] twice to kill it.

## WioLink Help

### How do I find my access_token
1. Open the WioLink app on your Phone ([Android](https://play.google.com/store/apps/details?id=cc.seeed.iot.ap&hl=en)) ([iOS](https://itunes.apple.com/us/app/wio-link/id1054893491?mt=8))
2. Select your device
3. Press the menu button on the upper right of the screen (3 vertical dots)
4. Select "View API"
5. Find the text "access_token=" followed by a long collection of random numbers and letters (this is your access_token)
6. Add your access_token to the ProtoConfig.py file

## Arduino Help

### How do I find my comPort
Linux:

    dmesg | grep tty

Mac:

    ls /dev/tty.*

### How do I communicate to the Server
Write data to serial port in a map format (distance: value, sound: value)
the server will need to deserialize this data.
