import random
# from telebot import TeleBot
import telebot
from os import getenv
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(getenv("TOKEN"))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Привет, я бот случайных чисел. Укажите диапазон чисел в формате /random_number <min> <max>")
    bot.register_next_step_handler(message, random_number)

def random_number(message):
    try:
        args = message.text.split()[1:]  
        if len(args) != 2:
            bot.send_message(message.chat.id, text="Пожалуйста, отправьте команду в формате /random_number <min> <max>")
            return
        
        min, max = int(args[0]), int(args[1])
        if min > max:
            bot.send_message(message.chat.id,)
        random_num = random.randint(min, max)

        
        bot.send_message(message.chat.id, f'Случайное число: {random_num}')

    except (ValueError, TypeError):
        bot.send_message(message.chat.id,text="Ошибка! Пожалуйста, укажите целочисленные значения для <min> и <max>")
        bot.register_next_step_handler(message,random_number)

bot.polling()
