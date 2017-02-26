#!/bin/bash
gnome-terminal \
--tab -e "mongod" \
--tab -e "python3 WioServer.py" \
--tab -e "python3 ArduinoServer.py" \
--tab -e "python3 FrontEndServer.py" \
--tab -e "python3 PushFrontEnd.py" \
--tab -e  "python3 DaoServer.py" \
--tab -e  "python3 PushServer.py" \
--tab -e  "python3 Reader.py"
