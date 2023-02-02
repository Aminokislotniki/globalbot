
import json


def post_lots(id_lot):

    f = open('lots/'+str(id_lot)+'.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    print(dict_lot)
    f.close()
    buf=''
    photo=""
    min_stavka=''
    times=''
    start_price = ''
    for z in dict_lot:
        for x in dict_lot[z]:
            if x=='lot_name':
                buf+='<b>Название: </b>' +str(dict_lot[z][x]).capitalize()+"\n"
            if x=="description":
                buf+='<b>Описание:  </b>'+str(dict_lot[z][x]).capitalize()+"\n"
            if x=="city":
                buf+='<b>Город:  </b>'+str(dict_lot[z][x]).capitalize() + "\n"
            if x=="delivery terms":
                buf+='<b>Условия доставки:  </b>'+str(dict_lot[z][x]).capitalize() + "\n"
            if x=="user_name_admin":
                buf+='<b>Продавец:  </b>' + '@'+str(dict_lot[z][x]) + "\n"
            if x=="start_price" and z=="lot_info":
                buf+='<b>Цена:  </b>'+str(dict_lot[z][x])+ "\n"
            if x=="photo":
                photo=(dict_lot[z][x])
            if x=="min_stavka":
                min_stavka=dict_lot[z][x]
            if x=="time_create":
                times=dict_lot[z][x]
            if x=="start_price":
                start_price=dict_lot[z][x]
    print(buf)
    return buf,photo,times,min_stavka,start_price



