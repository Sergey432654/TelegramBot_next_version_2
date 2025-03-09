import telebot
from telebot import types


bot = telebot.TeleBot(token='7472414373:AAF647-31cEXhFW-asmoig-0XT5PMNxEeD4')


user_data = {}
saved_data = {}

admin_user_id = '581487107'


@bot.message_handler(commands=['help'])
def line_call(call):
    bot.send_message(call.chat.id, f'Ось телеграм адміна цього бота @kirsan04')


@bot.message_handler(commands=['start'])
def start_handler(message):

    text = (
        "Привіт ✨\n"
        "На звʼязку Організація Поганого Гумору🥳\n"
        "Це бот, завдяки якому ти можеш зареєструватися на захід💫\n\n"
        "Який відбудеться: 05.10.24\n"
        "Час: 18:30, open door 18:00\n"
        "Місце: Sova Karaoke Bar in Košice\n"
        "Вхід: 5€, 20% з яких будуть передані на потреби ЗСУ🇺🇦"
    )


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    continue_button = types.KeyboardButton("Продовжити")
    markup.add(continue_button)


    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Продовжити")
def handle_continue(message):

    bot.send_message(message.chat.id, "Давай почнемо наше знайомство. Як тебе звуть? (Імʼя та прізвище)🤙")
    bot.register_next_step_handler(message, ask_participants)


def ask_participants(message):
    user_data[message.chat.id] = {'name': message.text}  # Зберігаємо ім'я користувача

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('1', callback_data='1'))
    markup.add(types.InlineKeyboardButton('2', callback_data='2'))
    markup.add(types.InlineKeyboardButton('3', callback_data='3'))
    markup.add(types.InlineKeyboardButton('4', callback_data='4'))
    markup.add(types.InlineKeyboardButton('Більше', callback_data='more_action'))  # Змінено на 'more_action'


    bot.send_message(message.chat.id, 'Виберіть кількість людей, які будуть з тобою (включно):', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.isdigit():
        user_data[call.message.chat.id]['participants'] = call.data
        finalize_registration(call.message)
    elif call.data == 'more_action':

        bot.send_message(call.message.chat.id, "Введіть точну кількість учасників:")
        bot.register_next_step_handler(call.message, handle_custom_count)


    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)


def handle_custom_count(message):
    try:
        count = int(message.text)
        user_data[message.chat.id]['participants'] = count
        finalize_registration(message)
    except ValueError:
        bot.send_message(message.chat.id, "Будь ласка, введіть коректне число.")


def finalize_registration(message):
    user_id = message.chat.id
    user_info = user_data.get(user_id, {})
    name = user_info.get('name')
    participants = user_info.get('participants')


    bot.send_message(message.chat.id,
                     f"Твоя реєстрація пройшла успішно✅\n"
                     f"Ім'я: {name}\n"
                     f"Кількість учасників: {participants}\n\n"
                     "Чекаємо на зустріч з тобою 😌\n\n"
                     "P.S: За 24 години до заходу тобі прийде підтвердження, "
                     "щоб впевнитися, що ти з нетерпінням чекаєш на наш розйобний стендап🥳")


    bot.send_message(admin_user_id, f"Користувач @{message.chat.username} зареєструвався:\nІм'я: {name}\nКількість учасників: {participants}")


    del user_data[user_id]


bot.polling(non_stop=True)
