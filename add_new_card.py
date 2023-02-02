import time
import json
from variables import bot,id_chanel
from datetime import datetime, timedelta
from keyboards import stavka1
import os


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

def information(call_id):
    bot.answer_callback_query(call_id, "Ставку можно отменить в течении 1 минуты, нажав на кнопку Отмена."
                                       "Выигранный лот необходимо выкупить в течении 5 дней, в противном случае БАН на 5 дней!!!", show_alert=True)

def  time_is_over_lot(lot_id,id_chanel,user_id,id,call_id):
    f= open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    time_lot_info = dict_lot['service_info']['time_create']
    channel_message_id = dict_lot["service_info"]["channel_message_id"]
    winner_finish = dict_lot['service_info']['winner_dict']
    data_winner = dict_lot['winner']
    lot_info = dict_lot['lot_info']
    f.close()
    time_today = (int(time.time()))
    time_break = ""
    a = 60*60
    print("время конца"+str(time_break))
    print("время сейчас"+str(time_today))
    for z in dict_lot:
        for x in dict_lot[z]:
            if x == "time_create":
                time_break += str(dict_lot[z][x])
    time_break = int(time_break) + a
    times = int(time_break) - time_today
    if times > 0:
        bot.answer_callback_query(call_id, "аукцион закончиться через \n " + convert_sec(times), show_alert=False)
    else:

        bot.answer_callback_query(call_id, "Аукцион уже закончен, участие невозможно,\n посмотрите другие лоты",
                                  show_alert=False)

    if time_today > time_break:
        print("hi")
        try:

            if "gold" in data_winner:
                winner_finish['user_name'] = data_winner['gold']['name_user']
                winner_finish['price_final'] = data_winner['gold']['price']
            with open('lots/' + str(lot_id) + '.json','w', encoding='utf-8') as f:
                json.dump(dict_lot,f,ensure_ascii=False,indent=15,)
            buf = ''
            buf += '<b>Название: </b>' + lot_info['lot_name'] + '\n'
            buf += '<b>Описание:  </b>' + lot_info['description'] + '\n'
            buf += '<b>Город:  </b>' + lot_info['city'] + '\n'
            buf += '<b>Условия доставки:  </b>' + lot_info['delivery terms'] + '\n'
            buf += '<b>Продавец:  </b>' + '@' + lot_info['user_name_admin'] + '\n\n'
            if 'user_name' in winner_finish:
                buf += '<b>       Победитель:  </b>' + ' 🥇'+ winner_finish['user_name'][0:3] + "***" + '\n'
                buf += '<b>💰Продано за :       </b>' +str(winner_finish['price_final']) + 'руб'
                bot.edit_message_caption(caption=buf, chat_id=id_chanel, message_id=channel_message_id, parse_mode="html")
                bot.send_photo(id, dict_lot["lot_info"]["photo"],
                               caption=buf, parse_mode="html")
        except TypeError:
            buf = ''
            buf += '<b>Название: </b>' + lot_info['lot_name'] + '\n'
            buf += '<b>Описание:  </b>' + lot_info['description'] + '\n'
            buf += '<b>Город:  </b>' + lot_info['city'] + '\n'
            buf += '<b>Условия доставки:  </b>' + lot_info['delivery terms'] + '\n'
            buf += '<b>Продавец:  </b>' + '@' + lot_info['user_name_admin'] + '\n\n'
            buf += '🏁 аукцион закончен.Победителей нет..'
            bot.edit_message_caption(caption=buf, chat_id=id_chanel, message_id=channel_message_id, parse_mode="html")
            bot.send_photo(id, dict_lot["lot_info"]["photo"],
                           caption=buf, parse_mode="html")


        with open('vocabulary/' + str(user_id) + '.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            active_lots = data['lots']
            arhive_lots = data['arhive']
            arhive_lots.append({"lot_id": str(lot_id), "lot_name": lot_info['lot_name']})
            for x in range(len(active_lots)):
                if active_lots[x]['lot_id'] == lot_id:
                    del active_lots[x]
                    break
        with open('vocabulary/' + str(user_id) + '.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, )
        src = 'E:/программирование/myglobalbot/lots/' + lot_id + '.json'
        dest = 'E:/программирование/myglobalbot/lots/lot_arhive/' + lot_id + '.json'
        os.rename(src, dest)
    else:
        pass






