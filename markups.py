from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from database.models import Category, Service

def main_markup(admin=False):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("Прайс услуг", callback_data="categories"),
        InlineKeyboardButton("Галерея", callback_data="galary"),
        InlineKeyboardButton("Записаться на услугу", callback_data="sign_up"),
        InlineKeyboardButton("Наш сайт", url="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiPqMnyiKCAAxU8JxAIHUjFBoEQyCl6BAggEAM&url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DdQw4w9WgXcQ&usg=AOvVaw0aHtehaphMhOCAkCydRLZU&opi=89978449")
    ]
    markup.add(*buttons)
    if admin:
        button=InlineKeyboardButton("админ панель",callback_data="admin_panel")
        markup.add(button)
    return markup


def services_markup(services: list[Service],  register: bool =False):
    markup = InlineKeyboardMarkup(row_width=2)
    for service in services:
        if register :
            button = InlineKeyboardButton(text=service.name, callback_data=f"register_service:/{service.id}")
        else:

            button = InlineKeyboardButton(text=service.name, callback_data=f"service:/{service.id}")
        markup.add(button)
    if register:
        back_button = InlineKeyboardButton(text="Назад к категориям", callback_data="back_to:/categories_register")
    else:
        back_button = InlineKeyboardButton(text="Назад к категориям", callback_data="back_to:/categories")
    markup.add(back_button)
    return markup


def categories_markup(categories: list[Category], register: bool=False):
    markup = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        if register:

            button = InlineKeyboardButton(text=category.name, callback_data=f"register_category:/{category.id}")
        else:
            button = InlineKeyboardButton(text=category.name, callback_data=f"category:/{category.id}")
        markup.add(button)
    
    return markup




def admin_markup():
    markup=InlineKeyboardMarkup(row_width=2)
    buttons= [
        InlineKeyboardButton("добавить услугу", callback_data="add_service"),
        InlineKeyboardButton("УДАЛИТЬ УСЛУГУ", callback_data="delete_service"),
        InlineKeyboardButton("просмотреть записи", callback_data="show_appointment"),
        InlineKeyboardButton("последние работы", callback_data="manage_last_work"),
        InlineKeyboardButton("добавить фото к галерею", callback_data="add_last_work")
    ]
        
    
    markup.add(*buttons)
    return markup


