import json
import requests
from math import ceil
import sys

issues = {
    "totalItems": 0,
    "Issues": []
}

search = input("Search term?")
start_date = input("Start date (yyyymmdd)?")
end_date = input("End date (yyyymmdd)?")
base_url= "https://chroniclingamerica.loc.gov/search/pages/results/"
page = 117
count = 1
row_size = 50
fails = 0
failed_pages = []

def dump_json(issues):
    issues["totalItems"] = count - 1
    with open(search + "_" + start_date + "_" + end_date + ".json", "w") as file:  
    #    JSON_data = json.load(file)
    #    JSON_data["totalItems"] += issues["totalItems"]          
        json.dump(issues, file)

def get_json(url, session, rows):
    payload = {'andtext':search, 'date1':start_date[0:4], 'date2':end_date[0:4], 'page':page, 'rows':str(rows), 'format':"json", 'dateFilterType':'yearRange'}
    try:
        data = session.get(url, params=payload, timeout=5)
#        print(data.content)
        json_file = json.loads(data.content)
    except requests.exceptions.ReadTimeout:
        raise requests.exceptions.ReadTimeout
    except json.decoder.JSONDecodeError:
        raise requests.exceptions.ReadTimeout
    else:
        return json_file

with requests.Session() as session:
    try:
        while True:
            try:
                total_items = get_json(base_url, session, 1)["totalItems"]
            except requests.exceptions.ReadTimeout:
                print("Timeout reached, retrying")
                continue
    #        except:
    #            print("Decode error, retrying")
    #            continue
            else:
                break

        total_pages = ceil(total_items/row_size)
        print(total_pages)

        while page < total_pages + 1:
            #if fails > 10:
             #   dump_json(issues)
              #  sys.exit()
            try:
                page_json = get_json(base_url, session, row_size)
                print(str(page) + " loaded.")
            except requests.exceptions.ReadTimeout:
                print(str(page) + " failed to load.")
                #page += 1
                fails += 1
                print(fails)
                if fails >= 5:
                    failed_pages.append(page)
                    page +=1
                    fails = 0
                continue
            else:
                fails = 0
                page += 1

            for record in page_json['items']:
                if record['date'] >= start_date and record['date'] <= end_date:
                    try:
                        new_record = {'item':count,'newspaper_title':record['title_normal'],'city':record['city'],'url':record['url'],'date':record['date'],'ocr_eng':record['ocr_eng']}
                    except KeyError:
                        print("Nonenglish ocr")
                    else:
                        issues["Issues"].append(new_record)
                        count += 1

    except KeyboardInterrupt:
        dump_json(issues)
        sys.exit()
    dump_json(issues)
    print("these pages failed to load")
    print(failed_pages)