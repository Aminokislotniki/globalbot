import time
import json
from variables import bot,id_chanel
from threading import *
from services_func import winner,winner_change_chanel
user_id = '958693574'
lot_id = '115'
def time_is_over_lot(lot_id,id_chanel,user_id):
    f = open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    time_lot_info = dict_lot['service_info']['time_create']
    channel_message_id = dict_lot["service_info"]["channel_message_id"]
    winner_finish = dict_lot['service_info']['winner_dict']
    data_winner = dict_lot['winner']
    lot_info = dict_lot['lot_info']
    f.close()
    time_today = (int(time.time()))

    a = 60*2
    time_break = int(time_lot_info) + a
    while True:
        try:
            print(time.time())
            time.sleep(5)
            if time_today > time_break:
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
                except TypeError:
                    buf = ''
                    buf += '<b>Название: </b>' + lot_info['lot_name'] + '\n'
                    buf += '<b>Описание:  </b>' + lot_info['description'] + '\n'
                    buf += '<b>Город:  </b>' + lot_info['city'] + '\n'
                    buf += '<b>Условия доставки:  </b>' + lot_info['delivery terms'] + '\n'
                    buf += '<b>Продавец:  </b>' + '@' + lot_info['user_name_admin'] + '\n\n'
                    buf += '🏁 аукцион закончен.Победителей нет..'
                    bot.edit_message_caption(caption=buf, chat_id=id_chanel, message_id=channel_message_id, parse_mode="html")
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

            else:
                pass
        except:
            pass


t1 = Thread(target=time_is_over_lot, args=(lot_id,id_chanel,user_id))

t1.start()

