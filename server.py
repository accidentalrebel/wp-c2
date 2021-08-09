#!/usr/bin/env python3

from wpc2 import *
from bs4 import BeautifulSoup
import urllib.parse
import hmac
import sys

AUTH_KEY = "0c008b2f27fbaf5e9acaaa08bf251fc98c6d38a1"
AUTH_SALT = "ea30c9849bfd208c9890cbf7bb56f59a20b52c4f"

time_slot = "0:00"
comment_index = 0
prev_unapproved_index = 0

def compute_moderation_hash(date_str):
    salt = AUTH_KEY + AUTH_SALT
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
      --compressed
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

    print(str(response))
    
    response_splitted = response.split("\n")
    response_details = response_splitted[-1]

    response_splitted = response_details.split(",")
    url = response_splitted[1]
    return get_unapproved_index_from_url(url)

if prev_unapproved_index == 0:
    delay_to_timeslot(time_slot)
    prev_unapproved_index = get_current_unapproved_index()
    print("## " + str(prev_unapproved_index))

# soup = BeautifulSoup(response_html, "html.parser")
# print(str(soup))

# response = submit_comment("TestComment")
# comment_index += 1

# response_splitted = response.split("\n")
# response_html = "\n".join(response_splitted[:-1])
# response_details = response_splitted[-1]

# response_splitted = response_details.split(",")
# http_code = response_splitted[0]
# url = response_splitted[1]

# print("## response html: " + response_html)
# print("## httpcode: " + http_code)
# print("## url: " + url);

# url_parsed = urllib.parse.urlparse(url)
# print("## " + str(url_parsed))
# print("## " + str(urllib.parse.parse_qs(url_parsed.query)))

# comments_page = fetch_comments_page(url)
# print("\n>>>\n\n")
# print(comments_page + "\n\n")

# computed_hash = compute_moderation_hash("2021-08-08 06:11:05")
# print("Computed hash: " + computed_hash)
