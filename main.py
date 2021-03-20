import telebot
import CONFIG

from TRIOL_lib import get_image_product, get_page_product, get_item_info

bot = telebot.TeleBot(CONFIG.TOKEN)


@bot.message_handler(content_types=["text"])
def send_info_product(message):
    id_item = message.text
    if len(id_item) > 9:
        # Ограничение на длину id товара более 9 знаков
        return 0

    bot.send_message(message.chat.id, get_item_info(id_item))
    bot.send_photo(message.chat.id, get_image_product(id_item))


if __name__ == '__main__':
    bot.infinity_polling()
