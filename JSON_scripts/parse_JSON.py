import json
import requests
from spellchecker import SpellChecker

JSON_file = input()
count = 1
JSON_data = None
spell = SpellChecker()


def get_json(url):
    data = requests.get(url)
    return(json.loads(data.content))

with open(JSON_file, "r") as file:            
    JSON_data = json.load(file)
    
print(JSON_data['totalItems'])

for issue in JSON_data["Issues"]:
    count += 1
    text = issue["ocr_eng"].split()
    total = len(text)

    misspelled = spell.unknown(text)
    wrong = len(misspelled)
    ratio = 1 - (wrong/total)
    issue["percentage"] = round(ratio,3)

    if count % 50 == 0:
        print(count)

with open(JSON_file, "w") as file: 
    json.dump(JSON_data, file)