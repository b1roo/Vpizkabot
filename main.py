from telebot import TeleBot
from config import BOT_TOKEN
from handlers.base_handlers import setup_base_handlers
from handlers.homework_handlers import setup_homework_handlers
from handlers.other_f_handlers import setup_other_files_handlers
from handlers.upload_handlers import setup_upload_handlers
from utils.keyboards import *
from admincons import setup_admin

bot = TeleBot(BOT_TOKEN)

setup_base_handlers(bot)
setup_homework_handlers(bot)
setup_admin(bot)
setup_other_files_handlers(bot)
setup_upload_handlers(bot)

@bot.message_handler()
def start_help_mes(message):
    bot.send_message(message.chat.id, information_data.start_text, parse_mode='MARKDOWN',
                     disable_web_page_preview=True)

if __name__ == "__main__":
    # print("Бот запущен...")
    bot.polling(none_stop=True)

