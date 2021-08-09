#!/usr/bin/env python3

from wpc2 import submit_comment, delay_to_timeslot
import datetime

seed = "abcdef"
commands = [ "info", "exfil", "delete" ]

target_blog = "http://127.0.0.3/"
sync_channel = "2021/08/06/hello-world/"

time_slot = "1:11"

delay_to_timeslot(time_slot)

print("Triggered at: " + str(datetime.datetime.now().time()))

response = submit_comment("TestComment2")
print(response)
