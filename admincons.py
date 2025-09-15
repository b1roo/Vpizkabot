import signal
import os
from telebot import types
import information_data
import subprocess

def setup_admin(bot):
    @bot.message_handler(commands=['checkid'])
    def check_id(message):
        bot.send_message(message.chat.id, message.from_user.id)

    @bot.message_handler(commands=['admin'])
    def admin_mess(message):
        cur_id = message.from_user.id
        if cur_id in information_data.admins_id:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text="Обновить бота на хосте (с перезагрузкой)", callback_data="git_upload"))
            keyboard.add(types.InlineKeyboardButton(text="Остановить работу бота (крайний случай)", callback_data="stop_bot"))
            keyboard.add(types.InlineKeyboardButton(text="Перезагрузить бота", callback_data="restart_bot"))
            # keyboard.add(types.InlineKeyboardButton(text="", callback_data=""))
            bot.send_message(message.chat.id, 'Выберете нужное действие:', reply_markup=keyboard)
        # else:
        #     bot.send_message(message.chat.id, 'У вас нат доступа к этой команде. \help', disable_web_page_preview=True)

    @bot.callback_query_handler(func=lambda call: call.data == 'git_upload')
    def git_upload(call):
        '''Обновление бота через git'''
        subprocess.run(['nohup', information_data.sh_path, 'git_upload', '&'])

    @bot.callback_query_handler(func=lambda call: call.data == 'restart_bot')
    def restart_bot(call):
        '''Рестарт работы бота'''
        subprocess.run(['nohup, "", 'restart_bot.sh', '&'])
        # print("./restart_bot.sh")


    @bot.callback_query_handler(func=lambda call: call.data == 'stop_bot')
    def stop_bot(call):
        '''Остановка работы бота'''
        bot.send_message(call.message.chat.id, 'Останавливаем работу бота...')
        os.kill(os.getpid(), signal.SIGINT)
