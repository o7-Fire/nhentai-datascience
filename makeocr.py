from PIL import Image

import pytesseract
import sharedutils


possible_languages = []
for v in sharedutils.filtered_id_to_language.values():
    if v not in possible_languages:
        possible_languages.append(v)

print(possible_languages)

DATA_DIR = "media/"

