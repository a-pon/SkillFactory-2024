import telebot
from config import TOKEN, currencies
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def show_help(message: telebot.types.Message):
    help_text = 'Список доступных валют: /currencies\n\nДля \
конвертации введите команду в слудующем формате:\n<название валюты> \
<в какую валюту перевести> <количество переводимой валюты>\n\n(Пример: \
доллар рубль 50.5)'
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['currencies'])
def show_currencies(message: telebot.types.Message):
    curr_text = 'Доступные валюты:'

    for c in currencies.keys():
        curr_text = '\n'.join((curr_text, c))

    bot.send_message(message.chat.id, curr_text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        user_input = message.text.lower().split(' ')

        if len(user_input) > 3:
            raise APIException('Слишком много параметров')

        if len(user_input) < 3:
            raise APIException('Недостаточно параметров')

        base, quote, amount = user_input
        total_quote = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        convert_text = f'Цена {amount} {currencies[base]} в {currencies[quote]} - {total_quote:.2f}'
        bot.send_message(message.chat.id, convert_text)


bot.polling()
