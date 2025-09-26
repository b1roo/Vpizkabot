import os
import sys
import time
import threading
import subprocess
from telebot import types
import information_data


def setup_admin(bot):
    @bot.message_handler(commands=['checkid'])
    def check_id(message):
        bot.send_message(message.chat.id, message.from_user.id)

    @bot.message_handler(commands=['admin'])
    def admin_mess(message):
        cur_id = message.from_user.id
        if cur_id in information_data.admins_id:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(
                text="❌ Остановить работу бота (обновление/рестарт)\n\nХост сам его перезапускает",
                callback_data="ask_stop_bot"))

            bot.send_message(message.chat.id, 'Выберете нужное действие:', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, '❌ У вас нет прав для выполнения данной команды!')

    # Обработчик подтверждения остановки
    @bot.callback_query_handler(func=lambda call: call.data == 'ask_stop_bot')
    def ask_stop_bot(call):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_stop_bot"),
            types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_action")
        )
        bot.edit_message_text(
            "🚨 ВЫ УВЕРЕНЫ, ЧТО ХОТИТЕ ОСТАНОВИТЬ БОТА?\n\n"
            "Это действие приведет к полной остановке работы бота!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )


    # Подтвержденная остановка
    @bot.callback_query_handler(func=lambda call: call.data == 'confirm_stop_bot')
    def confirm_stop_bot(call):
        bot.answer_callback_query(call.id, "🛑 Остановка...")
        bot.edit_message_text(
            "🛑 Останавливаю работу бота...\n\n"
            "Бот будет полностью выключен!",
            call.message.chat.id,
            call.message.message_id
        )
        threading.Timer(0, stop_bot_delayed).start()

    # Универсальная отмена
    @bot.callback_query_handler(func=lambda call: call.data == 'cancel_action')
    def cancel_action(call):
        bot.answer_callback_query(call.id, "❌ Действие отменено")

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            text="🔄 Перезагрузить бота (автообновление с git)",
            callback_data="ask_restart_bot"))
        keyboard.add(types.InlineKeyboardButton(
            text="❌ Остановить работу бота (крайний случай)",
            callback_data="ask_stop_bot"))

        bot.edit_message_text(
            f"❌ Действие отменено.\n\nВыберете нужное действие:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=keyboard
        )



def stop_bot_delayed():
    """Полная остановка бота"""
    time.sleep(2)
    print("🛑 Остановка по команде администратора...")
    os._exit(0)
