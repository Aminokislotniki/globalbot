import json

id_user = '958693574'
def del_lot_in_admin(id_user):
    with open('vocabulary/' + str(id_user) + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data1 = data['lots']
        for x in data1:
            id_lot = x["lot_id"]
            try:
                with open('lots/' + str(id_lot) + '.json', encoding='utf-8') as g:
                    g.close()
                    print('yes')
            except FileNotFoundError:
                for y in range(len(data1)):
                    if data1[y]['lot_id'] == id_lot:
                        del data1[y]
                        break
                with open('vocabulary/' + str(id_user) + '.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4, )
                f.close()













del_lot_in_admin(id_user)