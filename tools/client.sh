#!/bin/sh
cd ../src
python client.py -t "http://127.0.0.3/" -x "2021/08/13/exfil-channel/" -a "2021/08/13/ack-channel/" $@
