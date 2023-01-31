import json
id_user = '958693574'
lot_id = '72'

def migrac(id_user,lot_id):
    with open('vocabulary/' + str(id_user) + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data1 = data['lots']
    with open('lots/' + str(lot_id) + '.json', encoding='utf-8') as g:
        info = json.load(g)
        info = info['lot_info']['lot_name']
        data1.append({"lot_id": str(lot_id), "lot_name": info})
    with open('vocabulary/' + str(id_user) + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, )
    f.close()
    with open('vocabulary/' + str(id_user) + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data1 = data['not_posted_lots']
        for x in range(len(data1)):
            if data1[x]['lot_id'] == lot_id:
                del data1[x]
                break
    with open('vocabulary/' + str(id_user) + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, )
    f.close()
migrac(id_user,lot_id)