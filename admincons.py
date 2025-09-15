import signal
import os
from telebot import types
import information_data

def setup_admin(bot):
    @bot.message_handler(commands=['checkid'])
    def check_id(message):
        print(message.from_user.id)
        bot.send_message(message.chat.id, message.from_user.id)

    @bot.message_handler(commands=['admin'])
    def admin_mess(message):
        cur_id = message.from_user.id
        if cur_id in information_data.admins_id:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Обновить бота на хосте", callback_data="git_upload"))
            keyboard.add(types.InlineKeyboardButton(text="Остановить работу бота", callback_data="stop_bot"))
            keyboard.add(types.InlineKeyboardButton(text="ХЗ", callback_data="dunno"))
            bot.send_message(message.chat.id, 'Выберете нужное действие:', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'У вас нат доступа к этой команде. \help', disable_web_page_preview=True)
    @bot.callback_query_handler(func=lambda call: call.data == 'git_upload')
    def git_upload(call):
        '''Обновление бота через git'''
        return

    @bot.callback_query_handler(func=lambda call: call.data == 'stop_bot')
    def stop_bot(call):
        '''Остановка работы бота'''
        bot.send_message(call.message.chat.id, 'Останавливаем работу бота...')
        os.kill(os.getpid(), signal.SIGINT)
