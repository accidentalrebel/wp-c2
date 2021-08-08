#!/usr/bin/env python3

import subprocess
import urllib.parse
import hmac
import sys

AUTH_KEY = "0c008b2f27fbaf5e9acaaa08bf251fc98c6d38a1"
AUTH_SALT = "ea30c9849bfd208c9890cbf7bb56f59a20b52c4f"

def compute_moderation_hash(date_str):
    salt = AUTH_KEY + AUTH_SALT
    computed_hash = hmac.new(salt.encode(), date_str.encode(), 'md5').hexdigest()
    return computed_hash

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
    curl_command += comment_str + "' --compressed -Ls -o /dev/null -w \"%{http_code},%{url_effective}\""
    curl_output = subprocess.check_output(curl_command, shell=True)
    return curl_output.decode()

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

response = submit_comment("TestComment18")
response_splitted = response.split(",")
http_code = response_splitted[0]
url = response_splitted[1]

print("## httpcode: " + http_code)
print("## url: " + url);

url_parsed = urllib.parse.urlparse(url)
print("## " + str(url_parsed))
print("## " + str(urllib.parse.parse_qs(url_parsed.query)))

comments_page = fetch_comments_page(url)
print("\n>>>\n\n")
print(comments_page + "\n\n")

computed_hash = compute_moderation_hash("2021-08-08 06:11:05")
print("Computed hash: " + computed_hash)
