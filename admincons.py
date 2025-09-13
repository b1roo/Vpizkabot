from telebot import types
import information_data

def setup_admin(bot):
    @bot.message_handler(commands=['admin'])
    def admin_mess(message):
        cur_id = message.from_user.id
        if cur_id in information_data.admins_id:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text=f"Обновить бота на хосте", callback_data=f"git_upload"))
            keyboard.add(types.InlineKeyboardButton(text=f"ХЗ", callback_data=f"dunno"))
            bot.send_message(message.chat.id, 'Выберете нужное действие:', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'У вас нат доступа к этой команде. \help', disable_web_page_preview=True)
    @bot.callback_query_handler(func=lambda call: call.data.startswith('git'))
    def git(call):
        git_action = call.split('_')[1]
        #Сделать обработку сигналов для работы с git через бота
