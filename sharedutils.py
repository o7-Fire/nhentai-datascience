import os
import json
import time
import sys
from tqdm import tqdm
from multiprocessing import Pool

filter_tags = []  # ["lolicon", "rape"]
already_on_list = {}

filtered_id = []
filtered_id_ext = {}
filtered_id_to_id = {}
filtered_id_to_language = {}
id_to_data = {}

last_time_logging = time.time()
start_time = time.time()
index_failed = False
try:
    with open("filtered_id.csv", "r") as csv:
        text = csv.read()
        if len(text) > 0:
            filtered_id = filtered_id + text.split("\n")
        csv.close()

    with open("filtered_id_ext.json", "r") as f:
        filtered_id_ext = json.load(f)
        f.close()

    with open("filtered_id_to_id.json", "r") as f:
        filtered_id_to_id = json.load(f)
        f.close()

    with open("filtered_id_to_language.json", "r") as f:
        filtered_id_to_language = json.load(f)
        f.close()

    with open("id_to_data.json", "r") as f:
        id_to_data = json.load(f)
        f.close()

except Exception:
    index_failed = True
    pass

root_dir = "nhentai-data/g"


def process_jason(filename, ):
    if filename.endswith(".json"):
        i_be_seeth = os.path.join(root_dir, filename)
        with open(i_be_seeth) as json_file:
            data = json.load(json_file)
            # print(data['title'])
            required_tags = list(filter_tags)
            for tag in data['tags']:
                for filter_tag in required_tags:
                    if tag['name'] == filter_tag:
                        required_tags.remove(filter_tag)
            pretty_name = data['title']['pretty']
            if len(required_tags) == 0 and pretty_name not in already_on_list:
                try:
                    data['ext'] = os.path.splitext(data['cover']['src'])[1]
                    for language in data['languages']:
                        name = language['name']
                        if name != "translated":
                            data['language'] = name
                            break
                    if 'language' not in data:
                        data['language'] = None
                    return data
                except Exception:
                    # print("Error processing " + filename)
                    # print(json.dumps(data, indent=4, sort_keys=True))
                    return None
                # print(name)
                # print(iBeSeeth)


print(os.getcwd())

# {"id": 215433, "media_id": "1146377", "title": {"english": "(C86) [Karaage Of The Year (Karaage Muchio)] Otonamuke Mako Haru no Freedom na Matome (Free!)", "japanese": "(C86) [\u304b\u3089\u3042\u3052\u30aa\u30d6\u30b6\u30a4\u30e4\u30fc (\u304b\u3089\u3042\u3052\u3080\u3061\u304a)] \u5927\u4eba\u5411\u3051\u307e\u3053\u306f\u308b\u306e\u30d5\u30ea\u30fc\u30c0\u30e0\u306a\u307e\u3068\u3081 (Free!)", "chinese": null, "pretty": "Otonamuke Mako Haru no Freedom na Matome"}, "languages": [{"id": 6346, "type": "language", "name": "japanese", "url": "https://nhentai.net/language/japanese/", "count": 193003}], "cover": {"media_id": "1146377", "width": 350, "height": 494, "mime": "jpg", "src": "https://t.nhentai.net/galleries/1146377/cover.jpg"}, "url": "https://nhentai.net/g/215433", "tags": [{"id": 13400, "type": "group", "name": "karaage of the year", "url": "https://nhentai.net/group/karaage-of-the-year/", "count": 66}, {"id": 4079, "type": "artist", "name": "karaage muchio", "url": "https://nhentai.net/artist/karaage-muchio/", "count": 67}, {"id": 277, "type": "character", "name": "haruka nanase", "url": "https://nhentai.net/character/haruka-nanase/", "count": 580}, {"id": 491, "type": "character", "name": "makoto tachibana", "url": "https://nhentai.net/character/makoto-tachibana/", "count": 556}, {"id": 14283, "type": "tag", "name": "anal", "url": "https://nhentai.net/tag/anal/", "count": 65252}, {"id": 24726, "type": "tag", "name": "apron", "url": "https://nhentai.net/tag/apron/", "count": 2946}, {"id": 21712, "type": "tag", "name": "males only", "url": "https://nhentai.net/tag/males-only/", "count": 22405}, {"id": 7752, "type": "tag", "name": "schoolboy uniform", "url": "https://nhentai.net/tag/schoolboy-uniform/", "count": 12400}, {"id": 23895, "type": "tag", "name": "yaoi", "url": "https://nhentai.net/tag/yaoi/", "count": 28732}, {"id": 32687, "type": "parody", "name": "free", "url": "https://nhentai.net/parody/free/", "count": 999}, {"id": 33172, "type": "category", "name": "doujinshi", "url": "https://nhentai.net/category/doujinshi/", "count": 231184}, {"id": 6346, "type": "language", "name": "japanese", "url": "https://nhentai.net/language/japanese/", "count": 193003}]}

if index_failed:
    print("No Index")
    with Pool(8) as p:
        files_array = []
        for root, dirs, files in os.walk(root_dir):
            print("Found directory: %s" % root)
            print("Found %d files" % len(files))
            results = []
            for file in tqdm(files, desc="Processing files"):
                results.append(process_jason(file))
            deduped_results = []

            print("Found %d results" % len(results))
            print("Deduplicating")
            # dedupe
            for result in tqdm(results, desc="Deduplicating"):
                if result is None: continue
                name = result['title']['pretty']
                if name not in already_on_list:
                    already_on_list[name] = True
                    deduped_results.append(result)

            results = deduped_results

            for result in results:
                if result:
                    name = result['title']['pretty']
                    filtered_id.append(result['media_id'])
                    filtered_id_to_id[result['media_id']] = result['id']
                    filtered_id_to_language[result['media_id']] = result['language']
                    filtered_id_ext[result['media_id']] = result['ext']
                    id_to_data[result['id']] = result
                    if time.time() > (last_time_logging + 5):
                        logggg = str(len(already_on_list)) + " matches"
                        print(logggg)
                        last_time_logging = time.time()

print("Finished processing files")

if index_failed:
    print("Saving index")
    with open("filtered_id.csv", "w") as csv:
        csv.write("\n".join(filtered_id))
        csv.close()

    with open("filtered_id_ext.json", "w") as f:
        json.dump(filtered_id_ext, f)
        f.close()

    with open("filtered_id_to_id.json", "w") as f:
        json.dump(filtered_id_to_id, f)
        f.close()

    with open("filtered_id_to_language.json", "w") as f:
        json.dump(filtered_id_to_language, f)
        f.close()

    with open("id_to_data.json", "w") as f:
        stringed = json.dumps(id_to_data)
        f.write(stringed)
        f.close()

if len(filtered_id) == 0:
    print("Can't find shit on nhentai-data/g/")
    print("have you cloned the dataset ?")
    print("git clone https://github.com/shadow01148/nhentai-data --depth 1")
    sys.exit(1)
else:
    print("Found %d results" % len(filtered_id))


# i3.nhentai.net_galleries_988129_1.jpg
# 988129, 1, jpg

def files_media_to_media_id_page_ext(filename):
    split = filename.split("_")
    return split[2], split[3].split(".")[0], split[3].split(".")[1]
