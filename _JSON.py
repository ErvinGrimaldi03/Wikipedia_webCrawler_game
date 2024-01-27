import json

def save_json(data, name):
    with open(f"{name}.json", "w") as sd:
        json.dump(data, sd)


# x = open("Mario.json", encoding='utf8')
# d = json.load(x)
# for i in d['pages']:
#     print(i['title'])