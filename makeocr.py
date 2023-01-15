from PIL import Image

import pytesseract
import sharedutils
import os
import json

OUTPUT_DIR = "ocr/"

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

DATA_DIR = "media/"

filesPictures = os.listdir(DATA_DIR)\

# i3.nhentai.net_galleries_988129_1.jpg
for file in filesPictures:
    if file.endswith(".png") or file.endswith(".jpg"):

        (media_id, page, ext) = sharedutils.files_media_to_media_id_page_ext(file)
        language = sharedutils.filtered_id_to_language[media_id]
        if language not in languages_to_tesseract: continue
        if language not in desired_languages: continue
        print(file)
        print(language)
        output = pytesseract.image_to_data(Image.open(DATA_DIR + file), lang=languages_to_tesseract[language], output_type=pytesseract.Output.DICT)
        output['nhentai'] = {
            "id": sharedutils.filtered_id_to_id[media_id],
            "media_id": media_id,
            "page": page,
            "ext": ext,
            "language": language,

        }
        print(output["text"])
        print()

        with open(OUTPUT_DIR + file + ".json", "w") as f:
            json.dump(output, f)


