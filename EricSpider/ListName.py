import json
import sys
sys.path.insert(0, '/path/to/module/directory')
def get_names(filename):
    with open(filename, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
    names = [item['Name'] for item in data]
    return names