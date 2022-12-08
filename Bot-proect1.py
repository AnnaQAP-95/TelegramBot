import telebot
from configBot1 import keys,TOKEN
from utilsBot1 import  APIException,CryptoConverter



bot = telebot.TeleBot("5918342566:AAEIBAeT_ncuDkG1NlWFVfdR71Ijc4_5lYI")

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \n\
<в какую валюту перевести> \n \
<количество переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text',])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise  APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote,base,amount)
    except  APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e :
        bot.send_message(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id,text)

bot.polling()

