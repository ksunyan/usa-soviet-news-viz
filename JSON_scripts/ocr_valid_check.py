import json

JSON_file = input()
count = 0
JSON_data = None
average = 0
percentile_one = 0
percentile_two = 0
percentile_three = 0

with open(JSON_file, "r") as file:            
    JSON_data = json.load(file)

print(JSON_data['totalItems'])


for issue in JSON_data["Issues"]:
    count += 1
    percent = issue["percentage"]
    average += percent
    if percent >= .7:
        percentile_one += 1
    if percent >= .8:
        percentile_two += 1
    if percent >= .9:
        percentile_three

    if count % 1000 == 0:
        print(count)

    
average = average/JSON_data["totalItems"]

print(average)
print(percentile_one)
print(percentile_two)
print(percentile_three)