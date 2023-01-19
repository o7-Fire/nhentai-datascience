from PIL import Image
import PIL
import pytesseract
import sharedutils
import os
import json
from tqdm import tqdm
from multiprocessing import Pool
import idownloadedentirenhentaicdn

OUTPUT_DIR = "ocr/"
MEDIA_DATA_DIR = idownloadedentirenhentaicdn.DATA_DIR
REMOVE_IMAGE_THAT_NOT_INDEXED = False

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

filesPictures = idownloadedentirenhentaicdn.alreadyHere
alreadyHere = os.listdir(OUTPUT_DIR)


def process_ocr(file):
    if file.endswith(".png") or file.endswith(".jpg"):
        (media_id, page, ext) = sharedutils.files_media_to_media_id_page_ext(file)
        if media_id not in sharedutils.filtered_id_to_language:
            if REMOVE_IMAGE_THAT_NOT_INDEXED:
                os.remove(MEDIA_DATA_DIR + file)
            else:
                print("Skipping " + file + " because it's not in index")
            return
        language = sharedutils.filtered_id_to_language[media_id]
        if language not in languages_to_tesseract: return
        if language not in desired_languages: return
        filenOutputName = file + ".json"
        if filenOutputName in alreadyHere:
            # print("Skipping " + file + " because it's already done")
            return
        # print(file)
        # print(language)
        try:
            image = Image.open(MEDIA_DATA_DIR + file)
        except PIL.UnidentifiedImageError:
            os.remove(MEDIA_DATA_DIR + file)
            file = idownloadedentirenhentaicdn.http_get(media_id, page)
            try:
                image = Image.open(MEDIA_DATA_DIR + file)
            except PIL.UnidentifiedImageError:
                print("Da hood trying to download corrupted image but the downloaded image is corrupted" + str(file))
                return
        output = pytesseract.image_to_data(image, lang=languages_to_tesseract[language],
                                           output_type=pytesseract.Output.DICT)
        output['nhentai'] = {
            "id": sharedutils.filtered_id_to_id[media_id],
            "media_id": media_id,
            "page": page,
            "ext": ext,
            "language": language,
            'filename': file

        }
        # print(output["text"])
        # print()

        with open(OUTPUT_DIR + filenOutputName, "w") as f:
            json.dump(output, f)


with Pool(4) as p:
    r = list(tqdm(p.imap(process_ocr, filesPictures), total=len(filesPictures)))
