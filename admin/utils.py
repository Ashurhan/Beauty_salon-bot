from telebot import types, TeleBot
from markups import admin_markup
from settings import BOT as bot

from .markups import services_markup, appoinments_markup, del_photo_markup

from database import MANAGER as manager

from sqlalchemy.exc import DataError, IntegrityError


def admin_panel(call: types.CallbackQuery):
    text = "Привет, Админ!"

    markup = admin_markup()

    bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)


def show_services(call: types.CallbackQuery):
    text = "Выдан список услуг. Нажмите на определённую услугу, чтобы её удалить"

    services = manager.get_all_services()
    markup = services_markup(services=services)

    bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)


def delete_service(call: types.CallbackQuery):
    id_ = int(call.data.replace("service_delete:/", ""))
    manager.delete_service(id_)

    text = "Услуга удалена!"
    bot.send_message(chat_id=call.message.chat.id, text=text)


def pre_create_service(call: types.CallbackQuery):

    text = """
    Для того, чтобы добавить услугу, вам необходимо отправить сообщение с текстом услуги в данном формате:

    название услуги
    описание услуги
    цена на услугу (1500.00)
    номер категории (3)

    
    Для установки категории необходимо передать идентификационный номер категории:
    1 - ногти
    2 - волосы
    3 - макияж

    Отправте /stop для отмены действия
    """

    message_ = bot.send_message(chat_id=call.message.chat.id, text=text)
    bot.register_next_step_handler(message=message_, callback=create_service)


def create_service(message: types.Message):
    text = message.text

    if text == "/stop":
        bot.send_message(chat_id=message.chat.id, text="Действие отменено")
        return None
    
    text = text.split("\n")

    try:
        data = {
            "name": text[0],
            "description": text[1],
            "price": text[2],
            "category_id": text[3],
        }

        manager.insert_service(data=data)
    except (DataError, IndexError, IntegrityError):
        return re_create_service(message=message)
    else:
        bot.send_message(chat_id=message.chat.id, text="Успешно сохранено!")
        
    
def re_create_service(message: types.Message):
    text = "Неправильный формат данных. Удостоверьтесь, что отпрваленное сообщение соответсвует необходимому формату."
    message_ = bot.send_message(chat_id=message.chat.id, text=text)
    bot.register_next_step_handler(message=message_, callback=create_service)


def get_appointments(call:types.CallbackQuery):
    text="список всех существуещих записей" 
    appointments=manager.get_appointments()
    markup=appoinments_markup(appointments=appointments)
    bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

def get_appointment(call: types.CallbackQuery):
    id_=int(call.data.replace("appointment:/",""))
    appointment=manager.get_apoointment(appointment_id=id_)
    service=manager.get_service(service_id=appointment.service_id)
    link=f"http://t.me{appointment.username}"
    text=f"""
    {appointment.client} (@{appointment.username}) -{service.name}
    {appointment.time} 
    LINK TO USER :{link}
    """
    bot.send_message(chat_id=call.message.chat.id, text=text)


def show_last_works(call: types.CallbackQuery): 
    images = manager.get_last_works()
    if images:
        for image in images:
            markup = del_photo_markup(photo_id=image.id)
            bot.send_photo(chat_id=call.message.chat.id, photo=image.image, reply_markup=markup)
    else:
        bot.send_message(chat_id=call.message.chat.id, text="Галерея пуста")

def delete_last_work(call: types.CallbackQuery):
    id_=int(call.data.replace("last_work_delete:/",""))
    try:
        manager.delete_work(work_id=id_)
    except:
        pass
    finally:
        bot.send_message(chat_id=call.message.chat.id, text="удалено")

def pre_add_last_work(call: types.CallbackQuery):
    text = "Отправьте фотографию последней работы."

    message = bot.send_message(chat_id=call.message.chat.id, text=text)
    bot.register_next_step_handler(message=message, callback=add_last_work)


def add_last_work(message: types.Message):
    if message.content_type == "photo":
        photo_id = message.photo[-1].file_id
        photo_path = bot.get_file(photo_id).file_path
        photo = bot.download_file(photo_path)
        manager.insert_work_bytes(byte_code=photo)
        bot.reply_to(message=message, text="Сохранено!")
    else:
        bot.send_message(chat_id=message.chat.id, text="Ошибка!")

def register_handlers(bot: TeleBot):
    bot.register_callback_query_handler(admin_panel, func=lambda call: call.data=="admin_panel")
    bot.register_callback_query_handler(show_services, func=lambda call: call.data=="delete_service")
    bot.register_callback_query_handler(delete_service, func=lambda call: call.data.startswith("service_delete:/"))

    bot.register_callback_query_handler(pre_create_service, func=lambda call: call.data=="add_service")
    bot.register_callback_query_handler(get_appointments, func=lambda call: call.data=="show_appointment")
    bot.register_callback_query_handler(get_appointment, func=lambda call: call.data.startswith("appointment:/"))
    bot.register_callback_query_handler(show_last_works, func=lambda call: call.data=="manage_last_work")
    bot.register_callback_query_handler(delete_last_work, func=lambda call: call.data.startswith("last_work_delete:/"))
    bot.register_callback_query_handler(pre_add_last_work, func=lambda call: call.data=="add_last_work")






