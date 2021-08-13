import subprocess
import datetime
import time
import random
import string
import hmac

def submit_comment(url, comment_str):
    curl_command = "curl '" + url + "' ";
    curl_command += """-H 'Connection: keep-alive' \
      -H 'Cache-Control: max-age=0' \
      -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
      -H 'sec-ch-ua-mobile: ?1' \
      -H 'Upgrade-Insecure-Requests: 1' \
      -H 'Origin: http://127.0.0.3' \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36' \
      -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
      -H 'Sec-Fetch-Site: same-origin' \
      -H 'Sec-Fetch-Mode: navigate' \
      -H 'Sec-Fetch-User: ?1' \
      -H 'Sec-Fetch-Dest: document' \
      -H 'Referer: http://127.0.0.3/2021/08/06/hello-world/' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      --data-raw 'author=TestName&email=test%40email.com&url=&submit=Post+Comment&comment_post_ID=1&comment_parent=0&comment="""
    curl_command += comment_str + "' --compressed -Ls -w \"%{http_code},%{url_effective}\"" # -o /dev/null"
    curl_output = subprocess.check_output(curl_command, shell=True)
    return curl_output.decode()

def delay_to_timeslot(time_slot):
    # Waits until the next time slot

    current_date = datetime.datetime.utcnow()
    target_date = get_next_timeslot_date(current_date, time_slot)

    time_diff = target_date - current_date
    print("[INFO] Delaying for " + str(time_diff.seconds) + "." + str(time_diff.microseconds) + " or ~" + str(time_diff.seconds/60) + " mins")

    time.sleep(time_diff.seconds + (time_diff.microseconds / 1000000))

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

import datetime

# current_datetime = datetime.datetime.utcnow()

def get_next_timeslot_date(current_datetime, target_timeslot):
    print("## current_datetime: " + str(current_datetime))
    target_timeslot_splitted = target_timeslot.split(":")
    target_timeslot_minutes = int(target_timeslot_splitted[0])
    target_timeslot_seconds = int(target_timeslot_splitted[1])

    current_minute = current_datetime.time().minute
    print("## current_minute: " + str(current_minute))

    minute_offset = target_timeslot_minutes
    current_minute_end = current_minute % 10
    print("## current_minute_end:" + str(current_minute_end))

    if current_minute_end >=  target_timeslot_minutes:
            minute_offset += 10

    print("## minute_offset: " + str(minute_offset))
    current_minute_base = current_minute - (current_minute % 10)
    print("## current_minute_base: " + str(current_minute_base))
    next_datetime = current_datetime.replace(minute=current_minute_base, second=target_timeslot_seconds, microsecond=0)
    next_datetime += datetime.timedelta(minutes=minute_offset)
    print("## next_datetime: " + str(next_datetime))

    return next_datetime

def get_previous_valid_timeslot_date(current_datetime, time_slot):
    # Searches for the valid timeslot location within the previous 10 minutes
    ## For example with a time_slot of 1:11, 12:57:25 becomes 12:51:11, 12:50:00 becomes 12:41:11

    time_slot_splitted = time_slot.split(":")
    time_slot_minutes = int(time_slot_splitted[0])
    time_slot_seconds = int(time_slot_splitted[1])
    
    target_date = current_datetime
    
    target_hour = target_date.time().hour
    target_minute = target_date.time().minute
    target_minute -= 10;

    if target_minute < 0:
        target_minute = 60 + target_minute
        target_hour -= 1

    if (target_minute % 10) > time_slot_minutes:
        target_minute += 10
        if target_minute > 60:
            target_minute = target_minute - 60
            target_hour += 1

    target_minute = target_minute - (target_minute % 10) + time_slot_minutes
    target_date = target_date.replace(hour=target_hour, minute=target_minute, second=time_slot_seconds, microsecond=0)

    return target_date

def compute_moderation_hash(date_str, auth_key, auth_salt):
    salt = auth_key + auth_salt
    
    assert(salt == "0c008b2f27fbaf5e9acaaa08bf251fc98c6d38a1ea30c9849bfd208c9890cbf7bb56f59a20b52c4f")
    computed_hash = hmac.new(salt.encode(), date_str.encode(), 'md5').hexdigest()
    return computed_hash
