import telebot
from telebot import types

bot = telebot.TeleBot('8839701973:AAGGDHsXJS53yyrOO8IDJeyrHdM3xVETWG4')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("🛡️ الأمن السيبراني", callback_data="cyber")
    btn2 = types.InlineKeyboardButton("🤖 صنع بوتات", callback_data="bots")
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, "أهلاً بك! اختر قسماً:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    chat_id = call.message.chat.id
    if call.data == "cyber":
        bot.send_message(chat_id, "قائمة الأمن:\n@YG_EABOT\n@HCK11_bot")
    elif call.data == "bots":
        bot.send_message(chat_id, "قائمة صنع البوتات:\n@BotFather\n@MSNU1BOT")

bot.polling()

