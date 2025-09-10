from telebot import types
import information_data

def setup_base_handlers(bot):

    # Начальное сообщение со списком базовых команд
    @bot.message_handler(commands=['start', 'help'])
    def start_help_mes(message):
        bot.send_message(message.chat.id, information_data.start_text, parse_mode='MARKDOWN',
                         disable_web_page_preview=True)

    # Конспекты
    @bot.message_handler(commands=['notes'])
    def notes_mes(message):
        bot.send_message(message.chat.id, information_data.notes_text, parse_mode='MARKDOWN',
                         disable_web_page_preview=True)




