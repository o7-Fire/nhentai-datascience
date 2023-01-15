from PIL import Image

import pytesseract
import sharedutils
import os
import json
from tqdm import tqdm
from multiprocessing import Pool

OUTPUT_DIR = "ocr/"
MEDIA_DATA_DIR = "media/"

possible_languages = []
desired_languages = ["english"]
languages_to_tesseract = {
    "english": "eng",
    "japanese": "jpn",
    "chinese": "chi_sim",
}
for v in sharedutils.filtered_id_to_language.values():
    if v not in possible_languages:
        possible_languages.append(v)

print(possible_languages)

os.environ['OMP_THREAD_LIMIT'] = '1'

filesPictures = os.listdir(MEDIA_DATA_DIR)
alreadyHere = os.listdir(OUTPUT_DIR)

def process_ocr(file):
    if file.endswith(".png") or file.endswith(".jpg"):
        (media_id, page, ext) = sharedutils.files_media_to_media_id_page_ext(file)
        if media_id not in sharedutils.filtered_id_to_language:
            print("Skipping " + file + " because it's not in index")
            return
        language = sharedutils.filtered_id_to_language[media_id]
        if language not in languages_to_tesseract: return
        if language not in desired_languages: return
        filenOutputName = file + ".json"
        if filenOutputName in alreadyHere:
            #print("Skipping " + file + " because it's already done")
            return
        #print(file)
        #print(language)
        output = pytesseract.image_to_data(Image.open(MEDIA_DATA_DIR + file), lang=languages_to_tesseract[language],
                                           output_type=pytesseract.Output.DICT)
        output['nhentai'] = {
            "id": sharedutils.filtered_id_to_id[media_id],
            "media_id": media_id,
            "page": page,
            "ext": ext,
            "language": language,
            'filename': file

        }
        #print(output["text"])
        #print()

        with open(OUTPUT_DIR + filenOutputName, "w") as f:
            json.dump(output, f)


with Pool(4) as p:
    r = list(tqdm(p.imap(process_ocr, filesPictures), total=len(filesPictures)))
