#!/bin/sh
ps -ef | grep python[3] | cut -f 14,19,21 -d ' '
