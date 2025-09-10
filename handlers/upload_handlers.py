from telebot import types
import information_data
import os
from shared_data import file_cache
from shared_data import file_uploads
from shared_data import user_states


class UserState:
    WAITING_FILE = "waiting_file"
    WAITING_FILENAME = "waiting_filename"


def setup_upload_handlers(bot):


    @bot.callback_query_handler(func=lambda call: call.data.startswith('add_'))
    def add_file_handler(call):
        """Обработчик кнопки добавления файла"""
        data = call.data.split('_')
        subject = data[1]
        type = data[2]

        # Сохраняем информацию о том, куда добавляем файл
        user_id = call.from_user.id
        file_uploads[user_id] = {
            'subject': subject,
            'type': type,
            'state': UserState.WAITING_FILE
        }

        # Просим пользователя отправить файл
        bot.send_message(
            call.message.chat.id,
            f"📤 Отправьте файл, который хотите добавить в "
            f"{information_data.subjects_others[subject]} - "
            f"{information_data.file_types_others[type]}\n\n"
            f"⚠️ Файл будет сохранен с оригинальным названием",
            reply_markup=types.ForceReply(selective=True)
        )

    # Модифицируем обработчик документов
    @bot.message_handler(content_types=['document'])
    def handle_document(message):
        user_id = message.from_user.id

        if user_id not in file_uploads:
            bot.send_message(message.chat.id, "❌ Сначала выберите 'Добавить файл' в меню")
            return

        upload_info = file_uploads[user_id]
        subject = upload_info['subject']
        type = upload_info['type']

        # Обрабатываем каждый файл отдельно
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        target_dir = os.path.join(information_data.file_path_others, subject, type)
        os.makedirs(target_dir, exist_ok=True)

        filename = message.document.file_name
        file_path = os.path.join(target_dir, filename)

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Не очищаем состояние сразу - пользователь может отправить еще файлы
        bot.send_message(
            message.chat.id,
            f"✅ Файл '{filename}' добавлен. Отправьте еще файлы или нажмите /done для завершения"
        )

    # Добавляем команду для завершения загрузки
    @bot.message_handler(commands=['done'])
    def finish_upload(message):
        user_id = message.from_user.id
        if user_id in file_uploads:
            upload_info = file_uploads[user_id]
            subject = upload_info['subject']
            type = upload_info['type']

            # Показываем обновленный список
            show_updated_files(message.chat.id, subject, type)
            del file_uploads[user_id]
            bot.send_message(message.chat.id, "✅ Загрузка файлов завершена")
        else:
            bot.send_message(message.chat.id, "❌ Нечего завершать")

    def show_updated_files(chat_id, subject, type, reply_to_message_id=None):
        """Показать обновленный список файлов"""
        subject_name = information_data.subjects_others[subject]
        type_name = information_data.file_types_others[type]
        subject_type_path = os.path.join(information_data.file_path_others, subject, type)

        # Получаем обновленный список файлов
        files = []
        if os.path.exists(subject_type_path):
            files = [f for f in os.listdir(subject_type_path) if os.path.isfile(os.path.join(subject_type_path, f))]

        # Обновляем кэш
        cache_key = f"{subject}_{type}"
        file_cache[cache_key] = files

        keyboard = types.InlineKeyboardMarkup()

        for i, file in enumerate(files):
            keyboard.add(types.InlineKeyboardButton(
                text=f"📄 {file}",
                callback_data=f"oth_f_{subject}_{type}_{i}"
            ))

        keyboard.add(types.InlineKeyboardButton(
            text=information_data.add_file_text,
            callback_data=f"add_{subject}_{type}"
        ))

        keyboard.add(types.InlineKeyboardButton(
            text=information_data.back_text,
            callback_data=f"oth_subj_{subject}"
        ))

        bot.send_message(
            chat_id,
            f"📂 *{subject_name} - {type_name}*\n\nОбновленный список файлов:",
            parse_mode='Markdown',
            reply_markup=keyboard,
            reply_to_message_id=reply_to_message_id
        )

    @bot.message_handler(commands=['cancel'])
    def cancel_upload(message):
        """Отмена добавления файла"""
        user_id = message.from_user.id
        if user_id in file_uploads:
            del file_uploads[user_id]
            bot.send_message(message.chat.id, "❌ Добавление файла отменено")
        else:
            bot.send_message(message.chat.id, "❌ Нечего отменять")
