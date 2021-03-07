import telebot
import sqlite3
import CONFIG

bot = telebot.TeleBot(CONFIG.TOKEN)
a = []
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    a.append(message)
    id = message.text
    bot.send_message(message.chat.id, get_item_info(id))

def get_item_info(id) :
    con = sqlite3.connect('./TRIOL.db')
    cursor = con.cursor()
    cursor.execute('select name, description FROM Product where item_number = ' + id)
    out = cursor.fetchall()[0]
    return out[0] + '\n\n' + out[1]

if __name__ == '__main__':
     bot.infinity_polling()
