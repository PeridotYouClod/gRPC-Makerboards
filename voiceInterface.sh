#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS=$(realpath $(ls credentials/*.json))

gnome-terminal \
--tab -e "python3 ArduinoServer.py" \
--tab -e "python3 FrontEndServer.py" \
--tab -e "python3 GCloudConnector.py"
