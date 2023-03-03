import json
import pickle

json_source = input()
corpus_list = []

with open(json_source, "r") as file:            
    JSON_data = json.load(file)


for issue in JSON_data["Issues"]:
    if issue["percentage"] >= .9:
        corpus_list.append(issue["ocr_eng"])

    
count = len(corpus_list)

with open(json_source + "_" + str(count) + ".pickle", "wb") as file:
    pickle.dump(corpus_list, file)


    