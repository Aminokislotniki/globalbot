import json
from keyboards import edit_card_keyboard
from keyboards import quit_only_keyboard,stavka1
from lot_add import id_chanel
from post_lot import post_lots
from keyboards import stavka_canal,current_lots_keyboard
from datetime import datetime, timedelta
import os
import time
from variables import bot
from variables import active_lots

def dt_serj(s):
    s = s[2:]
    return s


def fs_serj(st):
    return(st[0:2])

#функция которая обновляет победителей в канале
def winner_change_chanel(lot_id, id_chanel):
    with open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        lot = data['lot_info']
        data_winner = data['winner']
    buf = ''
    buf += '<b>Название: </b>' + lot['lot_name'] + '\n'
    buf += '<b>Описание:  </b>' + lot['description'] + '\n'
    buf += '<b>Город:  </b>' + lot['city'] + '\n'
    buf += '<b>Условия доставки:  </b>' + lot['delivery terms'] + '\n'
    buf += '<b>Продавец:  </b>' + '@'+lot['user_name_admin'] + '\n\n'
    if "gold" in data_winner:
        buf += '🥇' + str(data_winner['gold']['price']) +' руб ' + ' -  ' + data_winner['gold']['name_user'][0:3] + "***" + '\n'
    if "silver" in data_winner:
        buf += '🥈' + str(data_winner['silver']['price']) +' руб ' + ' -  '  + data_winner['silver']['name_user'][0:3] + "***" + '\n'
    if "bronze" in data_winner:
        buf += '🥉' + str(data_winner['bronze']['price']) +' руб ' + ' -  '  + data_winner['bronze']['name_user'][0:3] + "***" + '\n'
    with open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8') as f:
        lot = json.load(f)
        f.close()
        channel_message_id = lot["service_info"]["channel_message_id"]
    bot.edit_message_caption(caption=buf, chat_id=id_chanel, message_id=channel_message_id,parse_mode="html",reply_markup=stavka_canal(lot_id))

def check_is_ban(user_id):
    # Возвращает FALSE - если бана нет.
    # Возвращает TRUE - если есть бан.
    # Если вдруг не нашло такого пользователя - записывает в JSON рыбу и возвращает FALSE
    f = open("users_statistics.json", 'r', encoding='utf-8')
    buf_statistics = json.loads(f.read())
    f.close()
    print(buf_statistics.keys())
    if str(user_id) in buf_statistics.keys():
        return buf_statistics[str(user_id)]["ban"]["is_ban"]
    else:
        buf_statistics[str(user_id)] = dict({"ban": {"is_ban": False, "time": 0}, "bets": []})
        with open('users_statistics.json', 'w', encoding='utf-8') as f:
            json.dump(buf_statistics, f, ensure_ascii=False, indent=4)
        print("Создан новый пользователь  ID=" + str(user_id))
        return False


def check_is_admin(user_id, bot):
    try:
        name_file = "vocabulary/" + str(user_id) + ".json"
        f = open(name_file, 'r', encoding='utf-8')
        f.close()
        return True
    except:
        bot.send_message(user_id, "Вы не являетесь Администратором")
        return False


def check_is_super_admin(user_id, bot):
    try:
        f = open("users_statistics.json", 'r', encoding="utf-8")
        buf = json.loads(f.read())
        super_admins = buf["super_admin_id"]
        if user_id in super_admins:
            return True
        else:
            bot.send_message(user_id,"Вы не являетесь Супер Администратором")
            return False
    except:
        print("что-то пошло не так в функции check_is_super_admin")

def id_lot():
    f = open("users_statistics.json", "r", encoding="utf-8")
    buf = json.loads(f.read())
    f.close()
    id = buf["lot_id"]
    buf["lot_id"] = id+1
    with open('users_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(buf, f, ensure_ascii=False, indent=4)
    return buf["lot_id"]

def view_card_of_lot(lot_id, bot, chat_id):
    print(lot_id)
    try:
        f = open("lots/" + str(lot_id) + ".json", "r", encoding="utf-8")
        lot = json.loads(f.read())
        f.close()
        text = f'<b>Название: </b>{lot["lot_info"]["lot_name"]}\n' \
               f'<b>Описание: </b>{lot["lot_info"]["description"]}\n' \
               f'<b>Город: </b>{lot["lot_info"]["city"]}\n' \
               f'<b>Условия доставки: </b>{lot["lot_info"]["delivery terms"]}\n' \
               f'<b>Продавец: </b>{lot["lot_info"]["user_name_admin"]}\n' \
               f'<b>Стартовая цена: </b>{lot["lot_info"]["start_price"]}\n' \
               f'<b>Актуальная цена: </b>{lot["lot_info"]["actual_price"]}\n'
        return text, lot


    except:
        bot.send_message(chat_id, "Какая-то хрень, но файл с ID - " + str(lot_id) + " не найден :(")
        return 0, 0

def edit_caption(message,bot, call, edit_part, id_lot, type_lot):
    if message.text == "/stop":
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_message(message.chat.id, "Вы вышли из редактирования", reply_markup=quit_only_keyboard)
    elif message.content_type == "text":
        old_caption = call.message.caption
        old_caption = old_caption.split("\n")
        for i in range(len(old_caption)):
            if edit_part in old_caption[i]:
                old_caption[i] = edit_part+ ": " + message.text
                break
        new_caption = "\n".join(old_caption)
        bot.edit_message_caption(caption=new_caption, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=edit_card_keyboard(id_lot,type_lot))
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id)

def save_new_caption_lot(caption, id_lot, admin_id, type_lot, bot, chat_id):
    names = ["Название", "Описание", "Город", "Условия доставки", "Стартовая цена"]
    keys = ["lot_name", "description", "city", "delivery terms", "start_price"]
    caption = caption.split("\n")
    new_data = dict()
    for i in range(len(names)):
        for x in caption:
            if names[i] in x:
                new_data[keys[i]] = x.replace((names[i]+": "), "")
    f = open("lots/" + str(id_lot) + ".json", "r", encoding="utf-8")
    lot = json.loads(f.read())
    f.close()
    lot["lot_info"].update(new_data)
    with open('lots/'+ id_lot + ".json", 'w', encoding='utf-8') as f:
        json.dump(lot, f, ensure_ascii=False, indent=4)

    lot_name_new = lot["lot_info"]["lot_name"]

    f = open("vocabulary/" + str(admin_id) + ".json", "r", encoding="utf-8")
    admin = json.loads(f.read())
    f.close()
    lots_list = admin[type_lot]
    for i in range(len(lots_list)):
        if lots_list[i]["lot_id"] == str(id_lot):
            admin[type_lot][i]["lot_name"] = lot_name_new
            break
    with open('vocabulary/'+ str(admin_id) + ".json", 'w', encoding='utf-8') as f:
        json.dump(admin, f, ensure_ascii=False, indent=4)
    bot.send_message(chat_id, "Лот " + lot_name_new + " успешно сохранен", reply_markup=quit_only_keyboard,parse_mode="html")


def post_to_channel_by_id(message,lot_id, bot,id_user):
    print(lot_id)
    if message.text == "/stop":
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id -1)
        bot.send_message(message.chat.id, "Вы вышли из отправки в канал, но вы можете продолжить редактировать лот", reply_markup=quit_only_keyboard)
    elif message.text == "/continue":
        with open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)

        n = bot.send_photo(id_chanel, data["lot_info"]["photo"], caption=post_lots(lot_id),
                       reply_markup=stavka_canal(lot_id),parse_mode="html")
        channel_message_id = n.json["message_id"]
        with open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8') as f:
            data1 = json.load(f)
        f.close()
        data1['service_info']['channel_message_id'] = channel_message_id
        with open('lots/' + str(lot_id) + '.json', 'w', encoding='utf-8') as f:
            json.dump(data1, f, ensure_ascii=False, indent=4)
        f.close()
        bot.send_message(message.chat.id, "Лот успешно опубликован")
        migrac(id_user,lot_id)
    else:
       msg = bot.send_message("Вы можете либо выйти через /stop\nЛибо подтвердить отправку через /continue")
       bot.register_next_step_handler(msg, post_to_channel_by_id, lot_id, bot)

def stavka_back(call_id,data):
    a = datetime.now()
    f = open('lots/' + str(data) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    f.close()
    for z in dict_lot:
        if z=="history_bets":
            mas_bets=dict_lot[z]
    print(mas_bets)
    for x in mas_bets:
        t = int(time.time())
        for i in range(len(mas_bets) - 1, -1, -1):
            if t - x[3] < 60:
                print(x)
                del mas_bets[i]
            # if (int(time.time())-x[3])<300:

            # bot.send_photo(call_id, dict_lot["lot_info"]["photo"], caption=dict_lot["lot_info"]["lot_name"]+"\n"+str(dict_lot["lot_info"]["start_price"])+"\n",
            #                 reply_markup=stavka1(data))
            # bot.delete_message(call.message.chat.id, call.message.message_id)
            winner(str(data))

            bot.answer_callback_query(call_id, "Ставка отменена успешно", show_alert=False)

            # for i in range(len(mas_bets)-1,-1,-1):
            #     print(mas_bets[i])
            #     del mas_bets[i]
        else:
            bot.answer_callback_query(call_id, "Ставкy отменить невозможно", show_alert=False)


#функция, которая делает миграцию лотов в json админа
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


#функция которая добавляет лот в json админа
def add_lots_of_admin(id_user,id_l):
        with open('vocabulary/' + str(id_user) + '.json','r', encoding='utf-8') as f:
            data = json.load(f)
            data1 = data['lots']
        f.close()
        with open('lots/' + str(id_l) + '.json', encoding='utf-8') as g:
            info = json.load(g)
            info = info['lot_info']['lot_name']
            data1.append({"lot_id": str(id_l), "lot_name": info})
        g.close()
        with open('vocabulary/' + str(id_user) + '.json','w', encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=4,)
        f.close()


def add_not_posted_lots_of_admin(id_user, id_l):
    with open('vocabulary/' + str(id_user) + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data1 = data['not_posted_lots']
    f.close()
    with open('lots/' + str(id_l) + '.json', encoding='utf-8') as g:
        info = json.load(g)
        info = info['lot_info']['lot_name']
        data1.append({"lot_id": str(id_l), "lot_name": info})
    g.close()
    with open('vocabulary/' + str(id_user) + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, )
    f.close()


def edit_card_in_channel(lot_id, bot, channel_id):
    with open('lots/' + str(lot_id) + '.json' , encoding='utf-8') as f:
        lot = json.load(f)
        f.close()
        channel_message_id = lot["service_info"]["channel_message_id"]

        names = ["Название", "Описание", "Город", "Условия доставки", "Продавец", "Актуальная цена"]
        keys = ["lot_name", "description", "city", "delivery terms","user_name_admin","actual_price"]
        caption = ""
        for i in range(len(names)):
            if lot["lot_info"][keys[i]] != None:
                caption +='<b>'+names[i]+'</b>' + ": " +str(lot["lot_info"][keys[i]]) + "\n"
            else:
                caption += names[i] + ": " + "нет данных" + "\n"
        bot.edit_message_caption(caption=caption, chat_id=channel_id, message_id=channel_message_id,
                                 reply_markup=stavka_canal(lot_id),parse_mode="html")

#ставка при первом нажатии участвовать
def stavka_lot(call_id,user_name,id,data):
    time_stavka = (int(time.time()))
    print(time_stavka)
    start_price = ""
    f = open('lots/' + str(data) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    f.close()
    for z in dict_lot:
        if z=="history_bets":
            mas_bets=dict_lot[z]
        for x in dict_lot[z]:
            if x == "start_price":
                start_price = int(dict_lot[z][x])
    if len(mas_bets) == 0:
        dict_lot["lot_info"]["actual_price"] = start_price
        dict_lot["history_bets"].append([id, user_name, start_price, time_stavka])

        with open('lots/' + str(data) + '.json', 'w', encoding='utf-8') as f:
            json.dump(dict_lot, f, ensure_ascii=False, indent=15)
        winner(data)
        buf = opisanie(str(data))
        bot.send_photo(call_id, dict_lot["lot_info"]["photo"], caption= buf, reply_markup=stavka1(data),parse_mode="html")
    else:
        winner(str(data))
        buf = opisanie(str(data))
        bot.send_photo(call_id, dict_lot["lot_info"]["photo"],
                       caption= buf,
                       reply_markup=stavka1(data),parse_mode="html")

#ставка с процентами
def percent_stavka(mas_st,user_name,call_id,id):
    time_stavka = (int(time.time()))
    user_name = user_name[0:3] + "***"
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

    actual_price_new=int(actual_price*float(mas_st[1])/100)+actual_price
    print(actual_price_new)
    if actual_price_new>actual_price:
        dict_lot["lot_info"]["actual_price"] = actual_price_new
        dict_lot["history_bets"] .append([id, user_name, actual_price_new,time_stavka])

        with open('lots/' + str(mas_st[0]) + '.json', 'w', encoding='utf-8') as f:
            json.dump(dict_lot, f, ensure_ascii=False, indent=15)
        winner(mas_st[0])
        buf = opisanie(mas_st[0])
        bot.send_photo(call_id, dict_lot["lot_info"]["photo"],
                       caption= buf, reply_markup=stavka1(mas_st[0]),parse_mode="html")

    else:
        bot.send_message(call_id, " Ваша ставка не принята\n " + str(actual_price) + user_name,
                         reply_markup=stavka1(mas_st[0]),parse_mode="html")

#ставка с цифрами
def dinamic_stavka(mas_st,user_name,id_user):
    time_stavka = (int(time.time()))
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
    dict_lot["history_bets"] .append ([id, user_name, actual_price_new,time_stavka])
    with open('lots/' + str(mas_st[0]) + '.json', 'w', encoding='utf-8') as f:
        json.dump(dict_lot, f, ensure_ascii=False, indent=15)
    winner(mas_st[0])
    buf = opisanie(str(mas_st[0]))
    bot.send_photo(id_user, dict_lot["lot_info"]["photo"],
                   caption=buf, reply_markup=stavka1(mas_st[0]),parse_mode="html")


def avtostavka(id,data,call_id,user_name):
    f = open('lots/' + str(data) + '.json', 'r', encoding='utf-8')
    dict_lot = json.loads(f.read())
    f.close()
    for z in dict_lot:
        if z=="history_bets":
            mas_bets=dict_lot[z]
    print(mas_bets)
    c=(len(mas_bets)-1)
    print(mas_bets[c])
    for i in mas_bets[c]:
        if id ==i:
            stavka_new=(mas_bets[c][2])+10
            print(stavka_new)
            time_stavka = (int(time.time()))
            mas_bets.append([id, user_name, stavka_new,time_stavka])
            dict_lot["history_bets"] = mas_bets

            with open('lots/' + str(data) + '.json', 'w', encoding='utf-8') as f:
                json.dump(dict_lot, f, ensure_ascii=False, indent=15)
            user_name = user_name[0:3] + "***"
            bot.send_message(call_id, " Ваша ставка принята\n " + str(stavka_new) + 'руб ' +user_name,
                             reply_markup=stavka1(data))
        else:
            bot.send_message(call_id, " Ваша ставка и так последняя\n ")

def list_active_lot_for_user(user_id, active_lots, bot):
    with open('users_statistics.json', encoding='utf-8') as f:
        all_users_stat = json.load(f)
        f.close()
        user_stat_bets = all_users_stat[str(user_id)]['bets']
        current_lots = dict()
        for x in user_stat_bets:
            if str(x['id_lot']) in active_lots.keys():
                current_lots[str(x['id_lot'])] = active_lots[str(x['id_lot'])]
        bot.send_message(user_id,"Вот ваши активные лоты:", reply_markup=current_lots_keyboard(current_lots))

def refresh_active_lots():
    for filename in os.listdir("vocabulary"):
        with open(os.path.join("vocabulary", filename), 'r', encoding='utf-8') as f:
            admin = json.load(f)
            for x in admin["lots"]:
                active_lots[x['lot_id']] = x['lot_name']
    print("Общий словарь активных лотов", active_lots)



#функция которая контролирует победителей и миграцию в файле лота
def winner(lot_id):
    with open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        data_list = data['history_bets']
        data_winner = data['winner']
    try:
        if data_list[-1] != []:
            data_winner.update({"gold": {"id_user": data_list[-1][0]}})
            data_winner["gold"].update({"name_user": data_list[-1][1]})
            data_winner["gold"].update({"price": data_list[-1][2]})
    except IndexError:
        if "gold" in data_winner:
            del data_winner["gold"]
        else:
            pass
    try:
        if data_list[-2] != []:
            data_winner.update({"silver": { "id_user": data_list[-2][0]}})
            data_winner["silver"].update({"name_user": data_list[-2][1]})
            data_winner["silver"].update({"price": data_list[-2][2]})
    except IndexError:
        if "silver" in data_winner:
            del data_winner["silver"]
        else:
            pass
    try:
        if data_list[-3] != []:
            data_winner.update({"bronze": { "id_user": data_list[-3][0]}})
            data_winner["bronze"].update({"name_user": data_list[-3][1]})
            data_winner["bronze"].update({"price": data_list[-3][2]})
    except IndexError:
        if "bronze" in data_winner:
            del data_winner["bronze"]
        else:
            pass

    with open('lots/' + str(lot_id) + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=15)
    f.close()

#функция удаляет ненужные лоты из файла админа
def del_lot_in_admin(id_user):
    try:
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
    except:
        pass

def opisanie (lot_id):
    with open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        lot = data['lot_info']
        data_winner = data['winner']
    buf = ''
    buf += '<b>Название: </b>' + lot['lot_name'] + '\n'
    buf += '<b>Описание:  </b>' + lot['description'] + '\n'
    buf += '<b>Город:  </b>' + lot['city'] + '\n'
    buf += '<b>Условия доставки:  </b>' + lot['delivery terms'] + '\n'
    buf += '<b>Продавец:  </b>' + '@'+lot['user_name_admin'] + '\n\n'
    if "gold" in data_winner:
        buf += '🥇' + str(data_winner['gold']['price']) +' руб ' + ' -  ' + data_winner['gold']['name_user'][0:3] + "***" + '\n'
    if "silver" in data_winner:
        buf += '🥈' + str(data_winner['silver']['price']) +' руб ' + ' -  '  + data_winner['silver']['name_user'][0:3] + "***" + '\n'
    if "bronze" in data_winner:
        buf += '🥉' + str(data_winner['bronze']['price']) +' руб ' + ' -  '  + data_winner['bronze']['name_user'][0:3] + "***" + '\n'
    with open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8') as f:
        lot = json.load(f)
        f.close()
    return buf