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
current_time = datetime.datetime.now().time()

time_diff = 0
if current_time.second < time_slot_seconds:
    time_diff = time_slot_seconds - current_time.second
else:
    time_diff = 60 - current_time.second + time_slot_seconds
    
print(str(current_time.second) + " ?- " + str(time_slot_seconds))
print(str(time_diff))

time.sleep(time_diff)

print("Triggering at: " + str(datetime.datetime.now().time()))

# response = submit_comment("TestComment1")
# print(response)
