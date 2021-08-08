#!/usr/bin/env python3

from wpc2 import submit_comment
import datetime
import time

seed = "abcdef"
commands = [ "info", "exfil", "delete" ]

target_blog = "http://127.0.0.3/"
sync_channel = "2021/08/06/hello-world/"

time_slot = "1:11"
time_slot_seconds = int(time_slot.split(":")[1])

current_date = datetime.datetime.now()

if current_date.time().second >= time_slot_seconds:
    target_date = current_date.replace(minute=current_date.time().minute + 1,second=time_slot_seconds, microsecond=0)
else:
    target_date = current_date.replace(second=time_slot_seconds, microsecond=0)

current_date = datetime.datetime.now()
    
time_diff = target_date - current_date
time.sleep(time_diff.seconds + (time_diff.microseconds / 1000000))

print("Triggering at: " + str(datetime.datetime.now().time()))

# response = submit_comment("TestComment1")
# print(response)
