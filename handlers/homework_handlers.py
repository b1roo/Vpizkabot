import urllib
from telebot import types
import information_data
import os
from utils.keyboards import create_homework_files_keyboard, get_homework_page_text

def setup_homework_handlers(bot):

    homework_pagination_cache = {}

    @bot.message_handler(commands=['hwfiles'])
    def hw_mes(message):

        keyboard = types.InlineKeyboardMarkup()  # Создание кнопок для каждого из предметов

        for subject_key, subject_name in information_data.subjects_homework.items():
            # Считаем количество файлов в папке предмета
            subject_path = os.path.join(information_data.file_path_homework, subject_key)
            file_count = 0
            if os.path.exists(subject_path):
                file_count = len([f for f in os.listdir(subject_path) if os.path.isfile(os.path.join(subject_path, f))])

            keyboard.add(types.InlineKeyboardButton(
                text=f"{subject_name} ({file_count} файлов)",
                callback_data=f"subject_{subject_key}"
            ))
        bot.send_message(message.chat.id, information_data.homework_files_text, reply_markup=keyboard)

    # Обработка нажатия на кнопку предмета для дз
    @bot.callback_query_handler(func=lambda call: call.data.startswith('subject_'))
    def show_files(call):
        subject = call.data.split('_')[1]
        subject_path = os.path.join(information_data.file_path_homework, subject)

        # Получаем список файлов
        files = []
        if os.path.exists(subject_path):
            files = [f for f in os.listdir(subject_path) if os.path.isfile(os.path.join(subject_path, f))]

        if not files:
            bot.send_message(
                chat_id=call.message.chat.id,
                text=f"📂 В папке '{information_data.subjects_homework[subject]}' пока нет файлов"
            )
            return

        # Сохраняем файлы в кэш для пагинации
        homework_pagination_cache[subject] = files
        page = 0  # Начинаем с первой страницы

        # Вычисляем общее количество страниц
        total_pages = (
                                  len(files) + information_data.HOMEWORK_FILES_PER_PAGE - 1) // information_data.HOMEWORK_FILES_PER_PAGE

        keyboard = create_homework_files_keyboard(files, subject, page)
        text = get_homework_page_text(files, information_data.subjects_homework[subject], page, total_pages)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('hwpage_'))
    def handle_homework_page_navigation(call):
        """Обработчик переключения страниц для домашних работ"""
        data = call.data.split('_')
        subject = data[1]
        page = int(data[2])

        # Получаем файлы из кэша
        if subject not in homework_pagination_cache:
            bot.answer_callback_query(call.id, "❌ Данные устарели")
            return

        files = homework_pagination_cache[subject]

        # Проверяем валидность страницы
        total_pages = (
                                  len(files) + information_data.HOMEWORK_FILES_PER_PAGE - 1) // information_data.HOMEWORK_FILES_PER_PAGE
        if page < 0 or page >= total_pages:
            bot.answer_callback_query(call.id, "❌ Неверная страница")
            return

        keyboard = create_homework_files_keyboard(files, subject, page)
        text = get_homework_page_text(files, information_data.subjects_homework[subject], page, total_pages)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    # Отправка файла
    @bot.callback_query_handler(func=lambda call: call.data.startswith('file_'))
    def send_file(call):
        """Отправить выбранный файл"""
        data = call.data.split('_')
        subject = data[1]
        encoded_filename = '_'.join(data[2:])  # На случай если в названии файла есть _
        filename = urllib.parse.unquote(encoded_filename)

        file_path = os.path.join(information_data.file_path_homework, subject, filename)

        try:
            with open(file_path, 'rb') as file:
                bot.send_document(call.message.chat.id, file)
            bot.answer_callback_query(call.id, "Файл отправлен 📄")
        except:
            bot.answer_callback_query(call.id, "❌ Файл не найден")

    # Кнопка назад к предметам
    @bot.callback_query_handler(func=lambda call: call.data == 'back_to_subjects')
    def back_to_subjects(call):
        """Вернуться к списку предметов"""
        hw_mes(call.message)
