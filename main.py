import telebot
from telebot import types #это позволит нам добавить кнопки и не только
import requests
import json


tocken = '5782454726:AAEc19f0oofh7I2GLhTrnF9qPDp48XLW3cA'
VAL_PRICE_URL_ = 'https://www.cbr-xml-daily.ru/daily_json.js'

#создаем объект приложения бота
bot = telebot.TeleBot(tocken)

is_file_ready = False #смогли ли мы загрузить данные из файла

data = dict()
try:
    with open("info.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    is_file_ready = True
except:
    is_file_ready = False

def get_currency(key_vallet):
    result = requests.get(VAL_PRICE_URL_)
    result = result.json()
    return [result['Valute'][key_vallet]['Name'], result['Valute'][key_vallet]['Value'], result['Valute'][key_vallet]['Previous']]

#обработчик сообщений
@bot.message_handler(commands=["start"])
def start(message):
    #print('!Это работет сообщение пришло!', message)
    markup = types.ReplyKeyboardMarkup() #типа клавиатура из кнопок
    button1 = types.KeyboardButton('😉 USD')
    button2 = types.KeyboardButton('EUR')
    markup.add(button1)
    markup.add(button2)
    if is_file_ready:
        for key in data.keys():
            button = types.KeyboardButton(key)
            markup.add(button)
    bot.send_message(message.from_user.id, 'Привет!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == '😉 USD':
        result = get_currency('USD')
        result_text = 'Валюта: ' + str(result[0]) + '\nТекущий курс: 😉 ' + str(result[1]) + '\nПрошлый курс: ' + str(result[2])
        bot.send_message(message.from_user.id, result_text)
    elif message.text == 'EUR':
        result = get_currency('EUR')
        result_text = 'Валюта: ' + str(result[0]) + '\nТекущий курс: ' + str(result[1]) + '\nПрошлый курс: ' + str(result[2])
        bot.send_message(message.from_user.id, result_text)
    else:
        if is_file_ready:
            for key in data.keys():
                if message.text in key:
                    result_text = 'Промокоды для ' + str(key) + '\n'
                    for element in data[key]:
                        result_text += '🔷' + ')'  
                        result_text += element 
                        result_text += "\n" 
                    bot.send_message(message.from_user.id, result_text)
        else:
            bot.send_message(message.from_user.id, 'Ошибка загрузки файла команд. К сожалению данная команда сейчас недоступна')


bot.polling(non_stop=True, interval=0)