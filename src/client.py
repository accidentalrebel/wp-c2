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

time_slot = "1:11"

delay_to_timeslot(time_slot)

print("Triggered at: " + str(datetime.datetime.now().time()))

random_string = generate_random_string(10)
response = submit_comment(target_blog, exfil_channel_id, random_string + ": Exfiltrated Data Test")
print(response)
