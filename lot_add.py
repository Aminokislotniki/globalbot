from variables import bot,id_chanel
import json
from keyboards import keyboard_lot_bot

lot_init_dict={}
dict_lot ={}
id_l=""


commands_user = ["/change_lot", "/change_description", "/change_price", "/change_min_stavka","/change_type_stavka","/admin_add","/view_lots"]
@bot.message_handler(commands=['new_lot'])
def star_new_lot(message):
    if message.text == "/new_lot":
        lot_init_dict[message.chat.id] = ""
        text = "Так будет выглядеть опубликованный лот\n Добавления нового лота:\n Остановить добавление: /stop\n\n Начнём - напишите  название лота\n\n"

        msg = bot.send_message(message.chat.id, text)
        photo = open(r"E:\программирование\myglobalbot\Снимок экрана 2023-01-28 214100.png", "rb")
        msg = bot.send_photo(message.chat.id, photo=photo, caption=text)

        bot.register_next_step_handler(msg, lot)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")


class Lot:
    def __init__(self, lot):
        self.lot = lot
        self.description = None
        self.city = None
        self.delivery_terms = None
        self.price = None
        self.min_stavka = None
        self.type_stavka = None
        self.photo = None

def lot_obj_lot(obj_lot):
    all_atributes = obj_lot.__dict__
    text = ""

    for key, value in all_atributes.items():
        val = value
        if key != "photo":
            if value == None:
                val = ""
            text = text + key + " : " + val + "\n"
    return text

def lot(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название лота")
        bot.register_next_step_handler(msg, lot)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")

    elif message.content_type == "text" and message.text.replace(" ", "") != "" and message.text not in commands_user:
        new_lot = Lot(message.text)
        lot_init_dict[message.chat.id] = new_lot
        dict_lot["lot_info"] = {}
        dict_lot["lot_info"].update({"lot_name": str(message.text).capitalize()})
        bot.send_message(message.chat.id, lot_obj_lot(lot_init_dict[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        msg = bot.send_message(message.chat.id,
                               "Теперь отправьте описание лота, \n/change_lot для редактирования названия лота, \nОстановить добавление:  /stop")
        bot.register_next_step_handler(msg, description)
    elif message.text in commands_user:
        msg = bot.send_message(message.chat.id, "что-то пошло не так, попробуй снова. \nПришли название лота")
        bot.register_next_step_handler(msg, lot)
    else:
        msg = bot.edit_message_text(message.chat.id,
                           "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_lot'")
        bot.register_next_step_handler(msg, lot)
def description(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название лота")
        bot.register_next_step_handler(msg, lot)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")
    elif message.text == "/change_lot":
        msg = bot.send_message(message.chat.id,"Введи новое название лота, \n\nОстановить добавление:  /stop")
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.register_next_step_handler(msg, lot)
    elif message.content_type == "text" and message.text.replace(" ", "") != "" and message.text not in commands_user:
        lot_init_dict[message.chat.id].description = message.text
        dict_lot["lot_info"].update({"description":str(message.text).capitalize()})
        bot.send_message(message.chat.id, lot_obj_lot(lot_init_dict[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        msg = bot.send_message(message.chat.id, "Теперь пришли локацию, где находиться лот")
        bot.register_next_step_handler(msg, city)

    else:
        msg = bot.send_message(message.chat.id,
                               "Ты неверно написал, напиши снова или\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_lot'")
        bot.register_next_step_handler(msg, description)

def city(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название лота")
        bot.register_next_step_handler(msg, lot)

    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")

    elif message.content_type == "text" and message.text.replace(" ", "") != "":
        lot_init_dict[message.chat.id].city = message.text
        dict_lot["lot_info"].update({"city":str(message.text).capitalize()})
        bot.send_message(message.chat.id, lot_obj_lot(lot_init_dict[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id-2)
        msg = bot.send_message(message.chat.id, "Опиши условия доставки")
        bot.register_next_step_handler(msg, delivery_terms)

    else:
        msg = bot.send_message(message.chat.id,
                           "Ты неверно написал, напиши снова или\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_lot'")
        bot.register_next_step_handler(msg, city)

def delivery_terms(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название лота")
        bot.register_next_step_handler(msg, lot)

    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")

    elif message.content_type == "text" and message.text.replace(" ", "") != "":
        lot_init_dict[message.chat.id].delivery_terms = message.text
        dict_lot["lot_info"].update({"delivery terms":str(message.text).capitalize()})
        bot.send_message(message.chat.id, lot_obj_lot(lot_init_dict[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)

        msg = bot.send_message(message.chat.id,
                               "Теперь отправьте цену лота \n/change_description для редактирования описания лота, \nОстановить добавление:  /stop")
        bot.register_next_step_handler(msg, price)
    else:
        msg = bot.send_message(message.chat.id,
                               "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_lot'")
        bot.register_next_step_handler(msg, delivery_terms)
def price(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название лота")
        bot.register_next_step_handler(msg, lot)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")
    elif message.text == "/change_description":
        msg = bot.send_message(message.chat.id, "Введи новое описание лота, \n\nОстановить добавление:  /stop")
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.register_next_step_handler(msg, description)
    elif message.content_type == "text" and message.text.replace(" ", "") != "" and message.text.isdigit() and message.text not in commands_user:
        lot_init_dict[message.chat.id].price = message.text
        dict_lot["service_info"]={}
        dict_lot ["lot_info"].update({"start_price":int(message.text)})
        dict_lot["service_info"].update({"start_price": int(message.text)})
        bot.send_message(message.chat.id, lot_obj_lot(lot_init_dict[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)


        msg = bot.send_message(message.chat.id,
                               "Теперь отправьте минимальную ставку \n/change_price для редактирования цены лота, \nОстановить добавление:  /stop")
        bot.register_next_step_handler(msg, min_stavka)
    else:
        msg = bot.send_message(message.chat.id,
                           "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_lot'")
        bot.register_next_step_handler(msg,price)

def min_stavka(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли Пришли название лота")
        bot.register_next_step_handler(msg, lot)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")
    elif message.text == "/change_price":
        msg = bot.send_message(message.chat.id, "Введи новую цену лота, \n\nОстановить добавление:  /stop")
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.register_next_step_handler(msg, price)
    elif message.content_type == "text" and message.text.replace(" ", "") != "" and message.text.isdigit() and message.text not in commands_user:
        lot_init_dict[message.chat.id].min_stavka = message.text
        dict_lot["service_info"].update({"min_stavka": int(message.text)})
        bot.send_message(message.chat.id, lot_obj_lot(lot_init_dict[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)

        msg = bot.send_message(message.chat.id,
                               "Теперь отправьте тип ставки:\n цифра '1'-% от стоимости (от 2 до 10, но не меньше) "
                               "минимальной ставки\n-или введи шаг ставки \n/change_min_stavka для редактирования минимальной ставки лота, \nОстановить добавление:  /stop")
        bot.register_next_step_handler(msg, type_stavka)
    else:
        msg = bot.send_message(message.chat.id,
                               "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_lot'")
        bot.register_next_step_handler(msg, min_stavka)
def type_stavka(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала.  Пришли название лота")
        bot.register_next_step_handler(msg, lot)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")
    elif message.text == "/change_min_stavka":
        msg = bot.send_message(message.chat.id, "Введи новую минимальную ставку лота, \n\nОстановить добавление:  /stop")
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.register_next_step_handler(msg, min_stavka)
    elif message.content_type == "text" and message.text.replace(" ", "") != ""and message.text.isdigit() and message.text not in commands_user:
        lot_init_dict[message.chat.id].type_stavka = message.text
        dict_lot["service_info"].update({"type_stavka":int(message.text)})
        bot.send_message(message.chat.id, lot_obj_lot(lot_init_dict[message.chat.id]))
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        msg = bot.send_message(message.chat.id, "Осталось загрузить фото \n/change_type_stavka для редактирования типа ставки лота, \nОстановить добавление:  /stop")
        bot.register_next_step_handler(msg, photo_lot)
    else:
        msg = bot.send_message(message.chat.id,
                               "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли '/new_lot'")
        bot.register_next_step_handler(msg, type_stavka)


def photo_lot(message):
    if message.text == "/new_lot":
        msg = bot.send_message(message.chat.id, "Начнём с начала. Пришли название лота")
        bot.register_next_step_handler(msg, lot)
    elif message.text == "/stop":
        bot.send_message(message.chat.id, "Вы вышли из добaвления лота")
    elif message.text == "/change_type_stavka":
        msg = bot.send_message(message.chat.id, "Введи новый тип ставки лота, \n\nОстановить добавление:  /stop")
        bot.register_next_step_handler(msg, type_stavka)
    elif message.content_type == "photo":
        photo1=( message.photo[-1].file_id)
        dict_lot["service_info"] .update( {"id_admin": message.from_user.id})
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.delete_message(message.chat.id, message.message_id - 2)
        bot.send_photo(message.chat.id, photo1,lot_obj_lot(lot_init_dict[message.chat.id]))
        dict_lot["lot_info"].update({"user_name_admin": message.from_user.username})
        dict_lot["lot_info"].update({'photo': photo1})
        bot.send_message(message.chat.id,
                         "Вот карточка лота.\nЧто делаем дальше?\nЕсли нужно что-то исправить выбери: \n /change_lot - изменение названия лота \n /change_description - изменение описания лота \n /change_price - изменение цены лота \n /change_min_stavka - изменение мин.ставки \n /change_type_stavka - изменение типа ставки \n Нажми сохранить\n Переходи в канал для опубликования: https://t.me/bot_final_auk\n"
                         "для создания нового лота пришли /new_lot", reply_markup=keyboard_lot_bot())

    else:
        msg = bot.send_message(message.chat.id,
                               "что-то пошло не так, попробуй снова\nДля выхода пришли '/stop'\nДля обновления карточки пришли /new_lot")
        bot.register_next_step_handler(msg, photo_lot)







