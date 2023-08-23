from telebot import TeleBot

from telebot import types

from dotenv import load_dotenv
from os import getenv, listdir

load_dotenv(".env")


from markups import (
    main_markup,
    services_markup,
    categories_markup,
)

from client_registration import register_handlers as client_handlers, start_states
from admin import register_handlers as admin_handlers

from settings import BOT as bot

from database import MANAGER as manager

admin_handlers(bot=bot)
client_handlers(bot=bot)





@bot.message_handler(commands=["start"])
def start(message: types.Message):
    text = """
    Привет,{message.from_user.username} пользователь! Рад тебя видеть.
    Я - телеграм бот салона красоты "Женские секреты"
    Я могу показать тебе наши последние работы, показать прайс услуг
    И зарегистрировать вас на какую-либо процедуру!

    Для более подробной информации отправьте команду /help
    """
    admin_id=int( getenv("ADMIN_TG_ID"))
    user_id=message.from_user.id
    if user_id==admin_id:
        markup=main_markup(admin=True)
    else:
        markup=main_markup()
   

    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(message: types.Message):
    text = """
    Comming soon!
    """

    bot.send_message(chat_id=message.chat.id, text=text)



@bot.callback_query_handler(lambda call: call.data=="categories")
def get_categories(call: types.CallbackQuery):
    text = """
    Выберите одну из категорий:
    """

    categories = manager.get_all_categories()
    markup = categories_markup(categories=categories)

    bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(lambda call: call.data.startswith("category:/"))
def get_services(call: types.CallbackQuery):
    id_ = int(call.data.replace("category:/", ""))
    services = manager.get_services_by_category(category_id=id_)
    markup = services_markup(services=services)

    text = f"Наши услуги по категории:"

    bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)



@bot.callback_query_handler(lambda call: call.data.startswith("service:/"))
def get_service(call: types.CallbackQuery):
    id_ = int(call.data.replace("service:/", ""))
    service = manager.get_service(service_id=id_)

    text = f"""
    {service.name} - от {service.price}
    {service.description}
    """

    bot.send_message(chat_id=call.message.chat.id, text=text)

   
@bot.callback_query_handler(lambda call: call.data.startswith("back_to:/"))
def back_to(call: types.CallbackQuery):
    to = call.data
    if to.endswith("categories"):
        return get_categories(call)
    elif to.endswith("categories_register") :
        return start_states(call)
    


@bot.callback_query_handler(lambda call: call.data=="galary")
def last_works(call: types.CallbackQuery): 
    images = manager.get_last_works()
    if len (images)==0:
        bot.send_message(chat_id=call.message.chat.id, text="Галерея пуста")
        return None

    for i  in range(0, len(images), 10):
        media = []
        for image in images[i:i+10]:
            image = types.InputMediaPhoto(image.image)
            media.append(image)
        
        bot.send_media_group(chat_id=call.message.chat.id, media=media)


if __name__ == "__main__":
    
    bot.infinity_polling()

    
