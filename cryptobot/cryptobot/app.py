import telebot
from config import keys, TOKEN
from exceptions import APIException, CryptoConvector

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = (' Чтобы начать работу с ботом необходимо ввести комманды в формате: \n<имя валюты, цену которой он хочет узнать>  \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\
Чтобы получить список доступных валют необходимо ввести комманд /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
       text = '\n'.join((text, key))

    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Ошибка ввода параметров!')

        quote, base, amount = values

        total = CryptoConvector.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена за {amount} {quote} будет - {total} {base}'
        bot.send_message(message.chat.id, text)

bot.polling()