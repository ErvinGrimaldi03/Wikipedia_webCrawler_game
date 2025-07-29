import json

def save_json(data, filename):
    try:
        with open(f"{filename}.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}.json")
    except IOError as e:
        raise IOError(f"Error saving JSON data to {filename}.json: {e}\n")

def load_json(filename):
    try:
        with open(f"{filename}.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename}.json not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {filename}.json: {e}")
        return None