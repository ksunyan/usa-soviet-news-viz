import json

JSON_file = input()
count = 0
JSON_data = None
average = 0
percentile_one = 0
percentile_two = 0
percentile_three = 0
lowest_score = 1
score_url = ""



with open(JSON_file, "r") as file:            
    JSON_data = json.load(file)

print(JSON_data['totalItems'])


for issue in JSON_data["Issues"]:
    count += 1
    percent = issue["percentage"]
    average += percent
    if percent >= .9:
        percentile_one += 1
    if percent >= .95:
        percentile_two += 1
    if percent >= .98:
        percentile_three += 1

    if percent < lowest_score:
        lowest_score = percent
        score_url = issue["url"]

    if count % 1000 == 0:
        print(count)

    
average = average/JSON_data["totalItems"]

print(average)
print(percentile_one)
print(percentile_two)
print(percentile_three)
print(lowest_score)
print(score_url)