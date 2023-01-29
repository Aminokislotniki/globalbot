import time
import json
from variables import bot
from datetime import datetime, timedelta

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

def stavka_back(call_id,b):
    a = datetime.now()
    if b>a:
        bot.answer_callback_query(call_id, "Ставка отменена успешно", show_alert=False)
    else:
        bot.answer_callback_query(call_id, "Ставкy отменить невозможно", show_alert=False)
