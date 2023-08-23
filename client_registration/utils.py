
from telebot import types, TeleBot
from sqlalchemy.exc import IntegrityError

from markups import (
    categories_markup,
    services_markup
)

from settings import BOT as bot
from database import MANAGER as manager

import datetime

users_states = []
    
STATE_ENTER_CATEGORY = 1
STATE_ENTER_SERVICE = 2
STATE_ENTER_NAME = 3
STATE_ENTER_DATE = 4



def start_states(call: types.CallbackQuery):
    try:
        user_ = [user for user in users_states if user.get("tg_id")==call.message.chat.id][0]
        users_states.remove(user_)
    except:
        pass

    user_data = {
        "tg_id": call.message.chat.id,
        "username": call.message.chat.username,
        "state": STATE_ENTER_CATEGORY
    }
    users_states.append(user_data)

    categories = manager.get_all_categories()
    markup = categories_markup(categories=categories, register=True)
    print(users_states)

    text = "Выберите категорию"
    bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=text, reply_markup=markup)


def enter_category(call: types.CallbackQuery):
    user_ = [user for user in users_states if user.get("tg_id")==call.message.chat.id][0]
    users_states.remove(user_)
    user_["state"]=STATE_ENTER_SERVICE
    users_states.append(user_)
    
    id_ = int(call.data.replace("register_category:/", ""))

    services = manager.get_services_by_category(category_id=id_)
    markup = services_markup(services=services, register=True)

    print(users_states)

    text = "Выберите услугу"
    bot.edit_message_text(message_id=call.message.id, chat_id=call.message.chat.id, text=text, reply_markup=markup)


def enter_service(call: types.CallbackQuery):
    id_ = int(call.data.replace("register_service:/", ""))
    user_ = [user for user in users_states if user.get("tg_id")==call.message.chat.id][0]
    users_states.remove(user_)
    user_["state"]=STATE_ENTER_NAME
    user_["service_id"] = id_
    users_states.append(user_)


    print(users_states)

    text = "Введите ваше ФИО"
    bot.send_message(call.message.chat.id, text=text)


def enter_name(message: types.Message):
    user_ = [user for user in users_states if user.get("tg_id")==message.chat.id][0]
    users_states.remove(user_)
    user_["state"] = STATE_ENTER_DATE 

    if user_.get("client") is None:
        name = message.text.strip()
        user_["client"] = name

    users_states.append(user_)
    print(users_states)

    text = "Введите дату и время в формате *2021-07-26 22:08*"
    bot.send_message(message.chat.id, text=text)


def enter_date(message: types.Message):
    date = message.text
    print(users_states)
    user_ = [user for user in users_states if user.get("tg_id")==message.chat.id][0]
    user_["time"] = date
    print(users_states)


    try:
        date_ = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text="Неправильно указан формат времени")
        return enter_name(message)
    else:
        if datetime.datetime.now() >= date_:
            bot.send_message(chat_id=message.chat.id, text="Дата должна быть в будущем времени!")
            return enter_name(message)
        elif date_.hour >= 21 or date_.hour < 8:
            bot.send_message(chat_id=message.chat.id, text="К сожалению введённое вами время не подходит для расписания работы салона. Открытие в 8:00, закрытие - 21:00")
            return enter_name(message)
    try:
        manager.insert_appointment(user_)
    except IntegrityError:
        bot.send_message(chat_id=message.chat.id, text="К сожалению в это время уже существует запись. Выберите другое.")
        return enter_name(message)

    users_states.remove(user_)
    bot.send_message(message.chat.id, text="OK")


def register_handlers(bot: TeleBot):
    bot.register_callback_query_handler(start_states, lambda call: call.data=="sign_up")
    bot.register_callback_query_handler(enter_category, lambda call: call.data.startswith("register_category:/") and [user for user in users_states if user.get("tg_id")==call.message.chat.id][0]["state"]==STATE_ENTER_CATEGORY)
    bot.register_callback_query_handler(enter_service, lambda call: call.data.startswith("register_service:/") and [user for user in users_states if user.get("tg_id")==call.message.chat.id][0]["state"]==STATE_ENTER_SERVICE)
    bot.register_message_handler(enter_name, func=lambda message: not message.text.startswith("/") and [user for user in users_states if user.get("tg_id")==message.chat.id][0]["state"]==STATE_ENTER_NAME)
    bot.register_message_handler(enter_date, func=lambda message: not message.text.startswith("/") and [user for user in users_states if user.get("tg_id")==message.chat.id][0]["state"]==STATE_ENTER_DATE)