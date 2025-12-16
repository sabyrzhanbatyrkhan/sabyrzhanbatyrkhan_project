#импорты времени и телебота
import telebot
import threading
import time

#токен бота и его подключение
token = "7532471716:AAGusFoU7OaTiuuOdlcSVedow-Vz_GdudfQ"
bot = telebot.TeleBot(token)

#сохраненки
user_data = {}

#старт
@bot.message_handler(commands="start")
def start_message(message):
  bot.send_message(message.chat.id,"Приветствую! Я Genuo, напоминалка о воде! Пожалуйста введите количество литров воды, которое вы должны выпить сегодня(чтобы добавить миллилитры просто напишите точку и количество, например: 3.2)")
  bot.register_next_step_handler(message,water_target)

def water_target(message):
  try:
    liter = float(message.text)*1000
    drunk_water = 0 
    user_data[message.chat.id] = {
    "liter": liter, 
    "drunkwater": drunk_water
}
    bot.reply_to(message,f"Хорошо! Вы должны выпить {liter} миллилитров за день! Отсчет пошел!\nКогда вы выпили воды введите /drank и количество миллилитров которое выпили.\nИспользуйте /status чтобы узнать, сколько воды еще нужно выпить в течений дня.\nА также не забудьте про напоминалку /setreminder и число, через часов которое оно будет напоминать вам попить воды!\nЧтобы поменять цель дня , просто введите /liter и новое значение миллилитров.")
    reminder1 = threading.Thread(target=day_time,args=(message.chat.id,)) #создание потока параллельного 
    reminder1.daemon = True #стоп потока при отключений(на крайний)
    reminder1.start() #старт потока
  except ValueError:
    bot.reply_to(message,"Напишите число!")
    bot.register_next_step_handler(message,water_target)
def day_time(chatid):
  while True:
    time.sleep(86400)
    if user_data[chatid]['liter'] <= user_data[chatid]['drunkwater']:
      bot.send_message(chatid,f'День закончен! Цель выполнена! Сегодня нужно выпить {user_data[chatid]["liter"]} мил')
    else:
      bot.send_message(chatid,f'День закончен! Цель не выполнена! Сегодня нужно выпить {user_data[chatid]["liter"]} мил')
    user_data[chatid]['drunkwater'] = 0

#питье
@bot.message_handler(commands="drank")
def drink_water(message):
  try:
    args = message.text.split()
    amount_water = float(args[1])
    user_data[message.chat.id]['drunkwater'] += amount_water
    bot.reply_to(message,f"Выпито {amount_water} миллилитров")
    if user_data[message.chat.id]['drunkwater'] >= user_data[message.chat.id]['liter']:
      bot.send_message(message.chat.id,f"Цель выполнена! {user_data[message.chat.id]['liter']} мил было выпито!")
  except KeyError:
    bot.reply_to(message,"Пожалуйста, для старта бота введите /start")
  except ValueError:
    bot.reply_to(message,"Пожалуйста , введите число(в мил)!")
  except IndexError:
    bot.reply_to(message,"Пожалуйста , введите число(в мил)!")
  
#статус
@bot.message_handler(commands="status")
def status(message):
  try:
    if user_data[message.chat.id]['liter'] <= user_data[message.chat.id]['drunkwater']:
      bot.send_message(message.chat.id, f"Ваша цель уже выполнена!")
    else:
      bot.send_message(message.chat.id, f"Осталось выпить: {user_data[message.chat.id]['liter'] - user_data[message.chat.id]['drunkwater']} миллилитров")
  except KeyError:
    bot.reply_to(message,"Пожалуйста, для старта бота введите /start")

#напоминалка
@bot.message_handler(commands="setreminder")
def reminder(message):
  try:
    args = message.text.split()
    hours = int(args[1])
    if "reminder_stop" in user_data.get(message.chat.id, {}):
      user_data[message.chat.id]["reminder_stop"].set()
    stop_event = threading.Event()
    user_data.setdefault(message.chat.id, {})["reminder_stop"] = stop_event
    status = user_data[message.chat.id]['liter'] - user_data[message.chat.id]['drunkwater'] #чисто для обработки keyerror
    bot.send_message(message.chat.id,f"Поставлено напоминание о воде через каждые {hours} часа")
    reminder2 = threading.Thread(target=hour_reminder,args=(message.chat.id,hours,status,stop_event)) #создание потока параллельного 
    reminder2.daemon = True #стоп потока при отключений(на крайний)
    reminder2.start() #старт потока
  except KeyError:
    bot.reply_to(message,"Пожалуйста, для старта бота введите /start")
  except ValueError:
    bot.reply_to(message,"Пожалуйста , введите число!")
  except IndexError:
    bot.reply_to(message,"Пожалуйста , введите число!")

def hour_reminder(chatid,hour,status,stop_event):
  while not stop_event.is_set():
    time.sleep(hour*3600)
    status = user_data[chatid]['liter'] - user_data[chatid]['drunkwater']
    if stop_event.is_set():
      break
    if status <= 0:
      return
    else:
      bot.send_message(chatid,f"Привет, не забывай пить воду! Нужно выпить еще {status} мил")

#замена цели
@bot.message_handler(commands="liter")
def set_liter(message):
  bot.reply_to(message,"Напишите новую цель!")
  bot.register_next_step_handler(message,set_user_data)
def set_user_data(message):
  try:
    liter = float(message.text)*1000
    user_data[message.chat.id]['liter'] = liter
    bot.send_message(message.chat.id,f"Новая цель: {liter} мил в день")
  except ValueError:
    bot.reply_to(message,"Введите число(например, 4.3)")
  except KeyError:
    bot.reply_to(message,"Пожалуйста, для старта бота введите /start")
  

#эхо функция, работает всегда
@bot.message_handler(func=lambda message:True)
def echo_all(message):
  bot.reply_to(message,"Неизвестная команда")

#запуск файла
if __name__ == "__main__":
  bot.polling() #и типо старт бота