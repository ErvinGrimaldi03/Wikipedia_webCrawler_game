import json

def save_json(data, name):
    with open(f"{name}.json", "w") as sd:
        json.dump(data, sd)