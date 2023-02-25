import json
import requests
from spellchecker import SpellChecker

JSON_file = input()
count = 1
JSON_data = None
spell = SpellChecker()
unicode_fail = 0

translation = {
    #"!" : ' ', "," : ' ', "." : ' ', ":" : " ", "_" : " ", "-" : ' ', "^" : ' ',
    #"\u2014" : ' ', "\u2019" : "\'" 
    "_" : " ", "!" : ' ', ":" : " "
}
table = str.maketrans(translation)

def get_json(url):
    data = requests.get(url)
    return(json.loads(data.content))

with open(JSON_file, "r") as file:            
    JSON_data = json.load(file)
    
print(JSON_data['totalItems'])

for issue in JSON_data["Issues"]:
    count += 1
    text = issue["ocr_eng"]
    try:
        text = str(bytes(text, "utf-8").decode("unicode_escape"))
    except UnicodeDecodeError:
        unicode_fail += 1
    text = text.translate(table)
    words = spell.split_words(text)
    total = len(words)

    misspelled = spell.unknown(words)
    wrong = len(misspelled)
    ratio = 1 - (wrong/total)
    issue["percentage"] = round(ratio,3)

    if count % 50 == 0:
        print(count)

print ( str(unicode_fail) + " ocr texts failed to decode in utf-8.")

with open(JSON_file, "w") as file: 
    json.dump(JSON_data, file)