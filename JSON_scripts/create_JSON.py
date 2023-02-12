import json
import requests
import csv

def get_json(url):
    data = requests.get(url)
    return(json.loads(data.content))

json_link = ""
count = 0

issues = {
    "Issues": {}
}

while True:
    json_link = input()
    if json_link== 'quit':
        break
    print(json_link)
    data = get_json(json_link)
    for record in data['issues']:
        if record['date_issued'] >= '1917-01-01' and record['date_issued'] < '1954-01-01':
            count += 1
            issues["Issues"][count] = record

    with open("valid_issues.json", "w") as file:
        json.dump(issues, file)
        