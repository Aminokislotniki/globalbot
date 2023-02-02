import json
import time
from threading import *
from variables import bot,id_chanel
from keyboards import type_of_lots_keyboard, active_lots_keyboard, nonpublic_lots_keyboard, card_view_keyboard, \
    edit_card_keyboard, arhive_lots_keyboard,stavka_canal, stavka
from services_func import fs_serj, dt_serj, check_is_admin, check_is_super_admin, \
    view_card_of_lot, edit_caption, save_new_caption_lot, post_to_channel_by_id, \
    id_lot,add_lots_of_admin,add_not_posted_lots_of_admin,edit_card_in_channel,avtostavka, \
    refresh_active_lots,list_active_lot_for_user,winner,winner_change_chanel,del_lot_in_admin, \
    stavka_back,stavka_lot,dinamic_stavka,percent_stavka,opisanie
from lot_add import star_new_lot,dict_lot
from admin_add import create_new_admin_json
from post_lot import post_lots
from add_new_card import time_lot,information,time_is_over_lot
from variables import active_lots

@bot.message_handler(commands=['start'])
def statistics(message):
    print(message.text)
    try:
        id_ll = (message.text)[7:]
        buf,photo,times,min_stavka,start_price=post_lots(id_ll)
        f = open("users_statistics.json", 'r', encoding='utf-8')
        buf_statistics = json.loads(f.read())
        f.close()
        if str(message.from_user.id) not in buf_statistics.keys():
            print("new user " + str(message.from_user.id))
            print(buf_statistics)
            buf_statistics[str(message.from_user.id)] = dict({"ban":"False", "bets":[]})

            with open('users_statistics.json', 'w', encoding='utf-8') as f:
                json.dump(buf_statistics, f, ensure_ascii=False, indent=4)

        else:
            # кусок else - можно убрать - чисто для проверки, что работает
            print("old user " + str(message.from_user.id))
        winner(id_ll)
        buf = opisanie(id_ll)
        bot.send_message(message.chat.id,
                         "Привет ,я бот аукционов Я помогу вам следить за выбранными лотами ,и регулировать ход аукциона.Удачных торгов 🤝 ")
        bot.send_photo(message.chat.id, photo=photo, caption=buf, reply_markup=stavka(id_ll),parse_mode="html")
    except:
        print("Что-то пошло не так в команде /start")

@bot.message_handler(commands=['new_lot'])
def new_lot():
    star_new_lot('new_lot')


@bot.message_handler(commands=['admin_add'])
def start_admin(message):
    if check_is_super_admin(message.from_user.id,bot):
        msg = bot.send_message(message.chat.id, "Перешлите сюда сообщение от человека, которого вы хотите добавить в Администраторы")
        bot.register_next_step_handler(msg, catch_reply)


def catch_reply(message):

    if message.content_type == "text" and message.text =="/stop":
        bot.send_message(message.chat.id, "Вы вышли из добавления администратора")
    elif not message.forward_from:
        msg = bot.send_message(message.chat.id, "Что-то пошло не так. Нужно Переслать сообщение от пользователя, которого вы хотите сделать админом\nПопробуйте снова\n напишите /stop - для выхода")
        bot.register_next_step_handler(msg, catch_reply)
    else:
        id = message.forward_from.id
        user_name = message.forward_from.username
        create_new_admin_json(id,user_name,bot,message.chat.id)

@bot.message_handler(commands=['current_lots'])
def current_lots(message):
    refresh_active_lots()
    list_active_lot_for_user(message.from_user.id, active_lots, bot)

@bot.message_handler(commands=['view_lots'])
def view_lots(message):
    # Проверка на админа
    if check_is_admin(message.from_user.id, bot):
        # теперь отправляем пользователю 3 кнопки
        bot.send_message(message.chat.id, "Выберите тип лота, который вы хотите просмотреть", reply_markup=type_of_lots_keyboard)

@bot.callback_query_handler(func=lambda call: True)
def call(call):
    print(call.data + " from " + call.from_user.username)
    flag = fs_serj(call.data)
    data = dt_serj(call.data)
    id = call.message.chat.id
    user_name = call.message.chat.username
    id_user = call.from_user.id


    if flag == "sc":
        if data[0] == "*":
            id_ll = data[1:]
            buf, photo, times, min_stavka, start_price = post_lots(id_ll)
            bot.send_photo(call.message.chat.id, photo=photo, caption=buf, reply_markup=stavka(id_ll))

    # Флаг для выхода из команды /view_lots
    if flag == "sq":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            print()

    # Флаг для возврата в меню выбора типа Лотов
    if flag =="ss":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберите тип лота, который вы хотите просмотреть", reply_markup=type_of_lots_keyboard)

    # Флаг для выброса Активнивных Лотов (parametr "lots")
    if flag =="sa":
        print(id_user)
        if data[0] =="*":
            page = data.split("*")
            page = int(page[1])
            try:
                name_file = "vocabulary/" + str(call.from_user.id) + ".json"
                f = open(name_file, 'r', encoding='utf-8')
                buf_admin_file = json.loads(f.read())
                f.close()
                active_lots = buf_admin_file['lots']

                if len(active_lots) > 0:
                    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id, text= "Выберете нужный лот\nстраница - " + str(page+1), reply_markup=active_lots_keyboard(active_lots, page))
                else:
                    bot.send_message(call.message.chat.id, "Активных лотов не найдено")
            except Exception:
                bot.send_message(call.message.chat.id, "Вы не создавали Лоты")

        if data[0] == ":":
            try:
                text_card, dict_lot_is = view_card_of_lot(data[1:], bot, call.message.chat.id)
                bot.send_photo(call.message.chat.id, dict_lot_is["lot_info"]["photo"], caption=text_card,parse_mode="html", reply_markup=card_view_keyboard(data[1:], "a"))
            except:
                bot.send_message(call.message.chat.id,"Что-то пошло не так")

    # Флаг для выброса Неопубликованных Лотов (parametr "not_posted_lots")
    if flag == "sn":
        if data[0] == "*":
            page = data.split("*")
            page = int(page[1])
            try:
                name_file = "vocabulary/" + str(call.from_user.id) + ".json"
                f = open(name_file, 'r', encoding='utf-8')
                buf_admin_file = json.loads(f.read())
                f.close()
                not_posted_lots = buf_admin_file['not_posted_lots']
                if len(not_posted_lots) > 0:
                    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          text="Выберете нужный лот\nстраница - " + str(page + 1),
                                          reply_markup=nonpublic_lots_keyboard(not_posted_lots, page))
                else:
                    bot.send_message(call.message.chat.id, "Неопубликованных лотов не найдено")
            except Exception:
                bot.send_message(call.message.chat.id, "Вы не создавали Лоты")

        if data[0] == ":":
            try:
                text_card, dict_lot_is = view_card_of_lot(data[1:], bot, call.message.chat.id)
                bot.send_photo(call.message.chat.id, dict_lot_is["lot_info"]["photo"], caption=text_card,parse_mode="html", reply_markup=card_view_keyboard(data[1:], "n"))
            except:
                bot.send_message(call.message.chat.id,"Что-то пошло не так")

    # Флаг для выброса Архивных Лотов (parametr "arhive")
    if flag =="sr":
        if data[0] == "*":
            page = data.split("*")
            page = int(page[1])
            try:
                name_file = "vocabulary/" + str(call.from_user.id) + ".json"
                f = open(name_file, 'r', encoding='utf-8')
                buf_admin_file = json.loads(f.read())
                f.close()
                arhive_lots = buf_admin_file['arhive']
                if len(arhive_lots) > 0:
                    bot.edit_message_text(message_id=call.message.message_id, chat_id=call.message.chat.id,
                                          text="Выберете нужный лот\nстраница - " + str(page + 1),
                                          reply_markup=arhive_lots_keyboard(arhive_lots, page))
                else:
                    bot.send_message(call.message.chat.id, "Неопубликованных лотов не найдено")
            except Exception:
                bot.send_message(call.message.chat.id, "Вы не создавали Лоты")

        if data[0] == ":":
            try:
                text_card, dict_lot_is = view_card_of_lot(data[1:], bot, call.message.chat.id)
                bot.send_photo(call.message.chat.id, dict_lot_is["lot_info"]["photo"], caption=text_card,parse_mode="html", reply_markup=card_view_keyboard(data[1:], "r"))


            except:
                bot.send_message(call.message.chat.id, "Что-то пошло не так")

    if flag =="se":
        if data[0] =="*":
            type_lot = data[1]
            id_lot_is = data.split(":")
            id_lot_is = id_lot_is[1]
            print(type_lot, id_lot_is)
            bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id, reply_markup=edit_card_keyboard(id_lot_is, type_lot))

        if data[0] == ":":
            type_lot = data[1]
            edit_part = data.split("?")
            edit_part = edit_part[1]
            text_list = call.message.caption.split("\n")
            lot_id = data[3:].split("?")
            lot_id = lot_id[0]
            print(type_lot, edit_part, lot_id)
            msg = bot.send_message(call.message.chat.id,"Для измениния поля - " + edit_part + ", отправьте сообщение в чат \nДля выхода напишите /stop")
            bot.register_next_step_handler(msg, edit_caption, bot, call, edit_part, lot_id, type_lot)

    if flag == "sw":
        print(data)
        if data[0] == "*":
            types = dict({"a": "lots", "n": "not_posted_lots", "r": "arhive"})
            temp = data.split(":")
            lot_id = temp[1]
            type_lot = temp[0].replace("*", "")
            type_lot = types[type_lot]
            caption = call.message.caption
            save_new_caption_lot(caption, lot_id, call.message.chat.id, type_lot, bot, call.message.chat.id)
            if type_lot == "lots":
                edit_card_in_channel(lot_id, bot, id_chanel)

    if flag =="sp":
        if data[0] =="*":
            lot_id = data.split("*")
            print("lot1" + data)
            lot_id = data[1:]
            print("lot2" + lot_id)
            alert_before_post = bot.send_message(call.message.chat.id,
                                   "Вы уверены что хотите опубликовать лот?\nЕсли вы не редактировали лот или не сохранили изменений кнопкой 'Сохранить' лот опубликуется без изменений\nДля выхода напишите /stop\nДля продолжение напишете /continue")
            bot.register_next_step_handler(alert_before_post, post_to_channel_by_id,lot_id, bot,id_user)

    if flag == "ls":
        lot_id = id_lot()

        bot.answer_callback_query(callback_query_id=call.id)
        dict_lot["lot_info"].update({"delivery_terms": None})
        dict_lot["service_info"].update({"message_id_in_channel": None})
        dict_lot["service_info"].update({"status": "activ"})
        dict_lot["service_info"].update({"time_create": (int(time.time()))})
        dict_lot["service_info"].update({"winner_dict": {"user_name": None, "price_final": None}})
        dict_lot["history_bets"] = []
        dict_lot["winner"] = {}

        with open('lots/' + str(lot_id) + '.json', 'w', encoding='utf-8') as f:
            json.dump(dict_lot, f, ensure_ascii=False, indent=15)
        with open('lots/' + str(lot_id) + '.json', 'r', encoding='utf-8') as f:
            list_lot = json.load(f)
            f.close()
            lot_price = list_lot['lot_info']['start_price']
        m = bot.send_photo(id_chanel, dict_lot["lot_info"]["photo"], caption=post_lots(lot_id),
                           reply_markup=stavka_canal(lot_id),parse_mode="html")
        channel_message_id = m.json["message_id"]
        dict_lot["service_info"]["channel_message_id"] = channel_message_id
        dict_lot["lot_info"].update({"actual_price": str(lot_price)})
        with open('lots/' + str(lot_id) + '.json', 'w', encoding='utf-8') as f:
            json.dump(dict_lot, f, ensure_ascii=False, indent=15)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        add_lots_of_admin(id_user, lot_id)
        bot.send_photo(id, dict_lot["lot_info"]["photo"],
                       caption="лот опубликован. Переходи в канал :" + id_chanel + "\n"
                               "для создания нового лота пришли '/new_lot'")
        del_lot_in_admin(id_user)
    # сборка лота
    if flag == "ld":
        bot.answer_callback_query(callback_query_id=call.id)
        bot.send_message(id, " попробуй снова, пришли '/new_lot'")
        dict_lot.clear()

    # ставка
    if flag == "ly":
        data = (call.data)[2:]
        print("flag ly" + data)
        winner(data)
        stavka_lot(id, user_name, id, data)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        winner(data)
        winner_change_chanel(data, id_chanel)



    if flag == "lf":
        mas_st=data.split('!')
        print("flag lf", mas_st)
        percent_stavka(mas_st,user_name,id,id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        winner(mas_st[0])
        winner_change_chanel(mas_st[0], id_chanel)

    # время
    if flag == "lt":
        data = (call.data)[2:]
        time_lot(call.id,data)

    # автоставка
    if flag == "li":
        information(call.id)

    if flag == "la": # клавиатура первого нажатия на участвовать. ставка равна начальной стоимости
        mas_st = data.split('!')
        print("mas_st" +mas_st)
        print("дата" + data)
        winner(data)
        dinamic_stavka(mas_st, user_name, id_user)
        winner(mas_st[0])
        winner_change_chanel(mas_st[0], id_chanel)

    # для отмены ставки
    if flag == "lb":
        print("qaewsxrctfvygbuh" +data)
        winner(data)
        stavka_back(call.id, data)
        winner(data)
        winner_change_chanel(data, id_chanel)

    if flag == "lo":
        bot.answer_callback_query(callback_query_id=call.id)
        dict_lot["lot_info"].update({"actual_price": None})
        dict_lot["lot_info"].update({"delivery_terms": None})
        dict_lot["service_info"].update({"message_id_in_channel": None})
        dict_lot["service_info"].update({"status": "activ"})
        dict_lot["service_info"].update({"time_create": (int(time.time()))})
        dict_lot["service_info"].update({"winner_dict": {"user_name": None, "price_final": None}})
        dict_lot["history_bets"] = []
        dict_lot["winner"] = {}
        dict_lot["service_info"]['channel_message_id'] = None
        id_l = id_lot()
        with open('lots/' + str(id_l) + '.json', 'w', encoding='utf-8') as f:
            json.dump(dict_lot, f, ensure_ascii=False, indent=4)
        add_not_posted_lots_of_admin(id_user, id_l)
        bot.delete_message(call.message.chat.id, call.message.message_id - 1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Лот добавлен в 'Неопубликованные', нажмите:  /view_lots для просмотра \n Переходи в канал :"  + id_chanel + " \nДля создания нового лота пришли '/new_lot' ")

    if flag=="lh":
        bot.answer_callback_query(callback_query_id=call.id)
        print(id)
        print(data)
        avtostavka(id,data,call.id,user_name)
        bot.send_message(call.message.chat.id, "Введи максимальную сумму")





print("Ready")
bot.infinity_polling()