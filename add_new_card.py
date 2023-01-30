import time
import json
from variables import bot
from datetime import datetime, timedelta
from keyboards import stavka1

def convert_sec(times):
    sec_to_min=60
    sec_to_hour=60*sec_to_min
    sec_to_day=24*sec_to_hour
    days=times//sec_to_day
    times %=sec_to_day
    hour = times//sec_to_hour
    times %= sec_to_hour
    min = times//sec_to_min
    times %= sec_to_min
    sec=times
    t=("\n%d дня, %d часа, %d минуты, %d секунды" % (days, hour, min, sec))
    return t
def time_lot(call_id,data):
    print(data)
    f = open('lots/'+ str(data) +'.json', 'r', encoding='utf-8')

    dict_lot = json.loads(f.read())
    print(dict_lot)
    f.close()
    time_today=(int(time.time()))
    time_break=""
    a=60*60*24*5
    for z in dict_lot:
        for x in dict_lot[z]:
            if x == "time_create":
                time_break += str(dict_lot[z][x])
    time_break=int(time_break)+a
    print(time_break)
    print(time_today)
    times = int(time_break)-time_today
    if times > 0:
        bot.answer_callback_query(call_id, "аукцион закончиться через \n "+convert_sec(times), show_alert=False)
    else:
        bot.answer_callback_query(call_id, "Аукцион уже закончен, участие невозможно,\n посмотрите другие лоты" , show_alert=False)

def information(call_id):
    bot.answer_callback_query(call_id, "Ставку можно отменить в течении 1 минуты, нажав на кнопку Отмена."
                                       "Выигранный лот необходимо выкупить в течении 5 дней, в противном случае БАН на 5 дней!!!", show_alert=True)

def stavka_back(call_id,data):
    a = datetime.now()
    f = open('lots/' + str(data) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    f.close()
    for z in dict_lot:
        if z=="history_bets":
            mas_bets=dict_lot[z]

#ставка при первом нажатии участвовать
def stavka_lot(call_id,user_name,id,data):
    time_stavka = datetime.now() + timedelta(minutes=1)
    print(time_stavka)
    start_price = ""
    f = open('lots/' + str(data) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    f.close()
    for z in dict_lot:
        for x in dict_lot[z]:
            if x == "start_price":
                start_price = int(dict_lot[z][x])
    dict_lot["lot_info"]["actual_price"] = start_price
    dict_lot["history_bets"].append([id,user_name,start_price])

    with open('lots/' + str(data) + '.json', 'w', encoding='utf-8') as f:
        json.dump(dict_lot, f, ensure_ascii=False, indent=15)
    user_name = user_name[0:3] + "***"
    bot.send_message(call_id, " Ваша ставка принята\n " + str(start_price) + user_name, reply_markup=stavka1(data))

#ставка с процентами
def percent_stavka(mas_st,user_name,call_id,id):
    actual_price = ""
    start_price = ""
    f = open('lots/' + str(mas_st[0]) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    f.close()
    for z in dict_lot:
        for x in dict_lot[z]:
            if x == "actual_price":
                actual_price = (dict_lot[z][x])
            if x == "start_price":
                start_price = (dict_lot[z][x])

    actual_price_new=int(start_price*float(mas_st[1])/100)+start_price
    print(actual_price_new)
    if actual_price_new>actual_price:
        dict_lot["lot_info"]["actual_price"] = actual_price_new
        dict_lot["history_bets"] .append([id, user_name, actual_price_new])


        with open('lots/' + str(mas_st[0]) + '.json', 'w', encoding='utf-8') as f:
            json.dump(dict_lot, f, ensure_ascii=False, indent=15)
        user_name = user_name[0:3] + "***"
        bot.send_message(call_id, " Ваша ставка принята\n " + str(actual_price_new) + user_name, reply_markup=stavka1(mas_st[0]))
    else:
        bot.send_message(call_id, " Ваша ставка не принята\n " + str(actual_price) + user_name,
                         reply_markup=stavka1(mas_st[0]))

#ставка с цифрами
def dinamic_stavka(mas_st,user_name,call_id,id):
    #print(data_st)
    actual_price = ""
    f = open('lots/' + str(mas_st[0]) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    f.close()
    for z in dict_lot:
        for x in dict_lot[z]:
            if x == "actual_price":
                actual_price = (dict_lot[z][x])
    actual_price_new = int(actual_price + float(mas_st[1]))
    print(actual_price)
    dict_lot["lot_info"]["actual_price"] = actual_price_new
    dict_lot["history_bets"] .append ([id, user_name, actual_price_new])
    with open('lots/' + str(mas_st[0]) + '.json', 'w', encoding='utf-8') as f:
        json.dump(dict_lot, f, ensure_ascii=False, indent=15)
    user_name = user_name[0:3] + "***"
    bot.send_message(call_id, " Ваша ставка принята\n " + str(actual_price_new) + user_name,
                     reply_markup=stavka1(mas_st[0]))

