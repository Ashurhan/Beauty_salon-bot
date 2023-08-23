from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup 
from database.models import Service

def services_markup(services : list [Service]):
    markup=InlineKeyboardMarkup(row_width=2)
    for service in services:
        button=InlineKeyboardButton(text=service.name, callback_data=f"services_delete:/{service.id}")
        markup.add(button)
    return markup
                                

def appoinments_markup(appointments):
    markup=InlineKeyboardMarkup(row_width=2)

    for appointment in appointments:
        button= InlineKeyboardButton(text=f"{appointment.time} - {appointment.client}",callback_data=f"appointment:/{appointment.id}")
        markup.add(button)
    return markup

def del_photo_markup(photo_id):
    markup=InlineKeyboardMarkup(row_width=1)
    button=InlineKeyboardButton(text="удалить",callback_data=f"last_work_delete:/{photo_id}")
    markup.add(button)

    return markup

