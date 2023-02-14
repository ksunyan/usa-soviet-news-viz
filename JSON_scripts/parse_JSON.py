import json
import requests

JSON_file = input()
count = 1
JSON_data = None


def get_json(url):
    data = requests.get(url)
    return(json.loads(data.content))

with open(JSON_file, "r") as file:            
    JSON_data = json.load(file)
    
print(JSON_data['totalItems'])

for issue in JSON_data["Issues"]:
    count+= 1
    text = issue["ocr_eng"].replace('\n','')
    issue["ocr_eng"] = text
    if count % 20 == 0:
        print(count)

with open(JSON_file, "w") as file:            
    json.dump(JSON_data, file)

