import os
import json
import time
import requests
import re
import zlib
import sys
import json
from multiprocessing import Pool
from urllib.parse import urlparse
from sharedutils import filtered_id, filtered_id_to_id, filtered_id_ext

DATA_DIR = "media/"

last_time_logging = time.time()
start_time = time.time()



print(time.time() - start_time)
print(filtered_id[1])
print(filtered_id_ext[filtered_id[1]])
print(filtered_id_to_id[filtered_id[1]])


def media_id_page_to_url(media_id, page):
    ext = filtered_id_ext[media_id]
    return "https://i3.nhentai.net/galleries/" + str(media_id) + "/" + str(page) + ext


def media_id_page_to_file(media_id, page):
    parsed_url = urlparse(media_id_page_to_url(media_id, page))
    return parsed_url.hostname + parsed_url.path.replace("/", "_").strip()


def http_get(media_id, page):
    ext = filtered_id_ext[media_id]
    url = "https://i3.nhentai.net/galleries/" + str(media_id) + "/" + str(page) + ext
    parsed_url = urlparse(url)
    # print(url)
    r = requests.get(url)
    # url = re.sub('[^0-9a-zA-Z.]+', '_', url)
    url = parsed_url.hostname + parsed_url.path.replace("/", "_")
    print(url)
    if r.status_code == 200:
        return url, r.content
    return None


print(http_get(filtered_id[1], 1)[0])

alreadyHere = os.listdir()
print("Already Here: " + str(len(alreadyHere)))


def transfer(id):
    page_counter = 1
    actual_id = filtered_id_to_id[id]
    results = []
    session = requests.Session()
    print(str(actual_id) + ": " + str(id))
    while True:
        filename = media_id_page_to_file(id, page_counter)
        page_counter = page_counter + 1
        if filename in alreadyHere: continue
        data = http_get(id, page_counter)
        if data is None: break
        f = open(DATA_DIR+filename, "wb")
        f.write(data[1])
        f.close()
        # results.append(upload(data, session))
    # return actual_id, results


print(transfer(filtered_id[1]))

with Pool(64) as p:
    transfer_results = p.map(transfer, filtered_id)
