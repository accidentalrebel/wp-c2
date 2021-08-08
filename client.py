#!/usr/bin/env python3

from wpc2 import submit_comment

seed = "abcdef"
commands = [ "info", "exfil", "delete" ]

target_blog = "http://127.0.0.3/"
sync_channel = "2021/08/06/hello-world/"

response = submit_comment("TestComment1")
print(response)
