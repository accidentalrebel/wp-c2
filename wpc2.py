import subprocess
import datetime
import time
import random
import string

def submit_comment(comment_str):
    curl_command = """
    curl 'http://127.0.0.3/wp-comments-post.php' \
      -H 'Connection: keep-alive' \
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
    
    time_slot_seconds = int(time_slot.split(":")[1])
    current_date = datetime.datetime.now()

    if current_date.time().second >= time_slot_seconds:
        target_date = current_date.replace(minute=current_date.time().minute + 1,second=time_slot_seconds, microsecond=0)
    else:
        target_date = current_date.replace(second=time_slot_seconds, microsecond=0)

    current_date = datetime.datetime.now()

    time_diff = target_date - current_date
    print("[INFO] Delaying for " + str(time_diff.seconds) + "." + str(time_diff.microseconds))

    time.sleep(time_diff.seconds + (time_diff.microseconds / 1000000))

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
