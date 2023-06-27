import telebot
from Config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}! Вы запустили Бота-Конвертера валют. Он может:  \n- Показать список доступных валют через команду /values \
    \n- Вывести конвертацию валюты через команду <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n \
- Нужна помощь? - Введите команду /help"
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nПример: Рубль Доллар 100 \nЧтобы увидеть список всех доступных валют, введите команду\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Ошибка в параметрах! Введите /help для того, чтобы узнать правильный вариант ввода')
        quote, base, amount = values
        total_base =CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message,f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Итого: {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id,text)
     #   total_base = Exchange.get_price(quote, base, amount)
  #  except ExchangeException as e:
   #     bot.reply_to(message, f'Ошибка пользователя.\n{e}')
  #  except Exception as e:
  #      bot.reply_to(message, f'Что-то пошло не так с {e}')
  #  else:
  #      text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
  #      bot.send_message(message.chat.id, text)
bot.polling(none_stop=True)