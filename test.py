import json

with open('lots/' + "136" + '.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    photo = data['lot_info']['photo']


