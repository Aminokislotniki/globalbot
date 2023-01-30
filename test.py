

#функция которая добавляет лот в json админа
def add_lots_of_admin(id_user,id_l):
        with open('vocabulary/' + str(id_user) + '.json','r', encoding='utf-8') as f:
            data = json.load(f)
            data1 = data['lots']
        with open('lots/' + str(id_l) + '.json', encoding='utf-8') as g:
            info = json.load(g)
            info = info['lot_info']['lot_name']
            data1.append({"lot_id": id_l, "lot_name": info})
            g.close()
        with open('vocabulary/' + str(id_user) + '.json','w', encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=4,)
            f.close()
