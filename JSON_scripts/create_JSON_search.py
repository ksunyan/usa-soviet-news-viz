import json
import requests
from math import ceil

issues = {
    "Issues": {}
}

search = input("Search term?")
start_date = input("Start date (yyyymmdd)?")
end_date = input("End date (yyyymmdd)?")
base_url= "https://chroniclingamerica.loc.gov/search/pages/results/"
page = 1
count = 1

def get_json(url, session):
    payload = {'andtext':search, 'date1':start_date[0:4], 'date2':end_date[0:4], 'page':page, 'rows':'100', 'format':"json", 'dateFilterType':'yearRange'}
    try:
        data = session.get(url, params=payload, timeout=1)
    except requests.exceptions.ReadTimeout:
        raise requests.exceptions.ReadTimeout
    else:
        return(json.loads(data.content))

with requests.Session() as session:

    while True:
        try:
            total_items = get_json(base_url, session)["totalItems"]
        except requests.exceptions.ReadTimeout:
            print("init connection failed, continuing")
            continue
        else:
            break

    total_pages = ceil(total_items/100)
    print(total_pages)

    while page < total_pages + 1:
        try:
            page_json = get_json(base_url, session)
        except requests.exceptions.ReadTimeout:
            print(str(page) + " failed to load.")
            page += 1
            continue
        else:
            page += 1

        for record in page_json['items']:
            print(record['date'])
            if record['date'] >= start_date and record['date'] <= end_date:
                try:
                    new_record = { count:{'url':record['url'],'date':record['date'],'ocr_eng':record['ocr_eng']}}
                except KeyError:
                    print("Nonenglish ocr")
                else:
                    issues["Issues"].update(new_record)
                    count += 1


    with open(search + "_" + start_date + "_" + end_date + ".json", "w") as file:            
        json.dump(issues, file)