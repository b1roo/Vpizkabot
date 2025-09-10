from telebot import types
import information_data
import os
from shared_data import file_cache
from utils.keyboards import create_files_keyboard, get_page_text

def setup_other_files_handlers(bot):

    pagination_cache = {}

    def get_files_text(files):
        """Генерируем текст в зависимости от количества файлов"""
        if not files:
            return "❌ Файлов не найдено\n\n📤 Вы можете добавить первый файл!"
        elif len(files) == 1:
            return "Найден 1 файл:"
        else:
            return f"Найдено {len(files)} файлов:"

    @bot.message_handler(commands=['allfiles'])
    def all_mes(message):
        """Главное меню всех файлов"""
        keyboard = types.InlineKeyboardMarkup()

        keyboard.add(types.InlineKeyboardButton(
            text='📁 Просмотреть все файлы',
            callback_data='look_all_files'
        ))

        keyboard.add(types.InlineKeyboardButton(
            text='🔍 Найти файлы по предмету',
            callback_data='find_by_subject'
        ))

        keyboard.add(types.InlineKeyboardButton(
            text='📤 Загрузить файл',
            callback_data='upload_file'
        ))

        bot.send_message(message.chat.id, information_data.all_files_text,
                         reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: call.data == 'find_by_subject')
    def find_by_subject(call):
        """Выбор предмета для поиска файлов"""
        keyboard = types.InlineKeyboardMarkup()

        for subject_key, subject_name in information_data.subjects_others.items():
            keyboard.add(types.InlineKeyboardButton(
                text=f"{subject_name}",
                callback_data=f"oth_subj_{subject_key}"
            ))

        keyboard.add(types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="back_to_allfiles_menu"
        ))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите предмет:",
            reply_markup=keyboard
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('oth_subj_'))
    def choose_file_type(call):
        """Выбор типа файлов для выбранного предмета"""
        subject_key = call.data.split('_')[2]  # получаем ключ предмета
        subject_name = information_data.subjects_others[subject_key]

        keyboard = types.InlineKeyboardMarkup()

        for type_key in information_data.in_others_key:
            type_path = os.path.join(information_data.file_path_others, subject_key, type_key)
            file_count = 0

            if os.path.exists(type_path):
                file_count = len([f for f in os.listdir(type_path)
                                  if os.path.isfile(os.path.join(type_path, f))])

            type_name = information_data.file_types_others[type_key]
            keyboard.add(types.InlineKeyboardButton(
                text=f"{type_name} ({file_count} файлов)",
                callback_data=f"oth_tp_{subject_key}_{type_key}"
            ))

        keyboard.add(types.InlineKeyboardButton(
            text="◀️ Назад к предметам",
            callback_data="find_by_subject"
        ))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"📚 {subject_name}\n\nВыберите тип файлов:",
            reply_markup=keyboard
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith('oth_tp_'))
    def show_other_files(call):
        try:
            data = call.data.split('_')
            subject = data[2]
            type = data[3]
            page = 0  # По умолчанию первая страница

            subject_name = information_data.subjects_others[subject]
            type_name = information_data.file_types_others[type]

            subject_type_path = os.path.join(information_data.file_path_others, subject, type)

            # Получаем список файлов
            files = []
            if os.path.exists(subject_type_path):
                files = [f for f in os.listdir(subject_type_path) if os.path.isfile(os.path.join(subject_type_path, f))]

            # Сохраняем в кэш
            cache_key = f"{subject}_{type}"
            file_cache[cache_key] = files
            pagination_cache[cache_key] = files  # Для пагинации

            # Вычисляем общее количество страниц
            total_pages = (len(files) + information_data.FILES_PER_PAGE - 1) // information_data.FILES_PER_PAGE

            keyboard = create_files_keyboard(files, subject, type, page)
            text = get_page_text(files, subject_name, type_name, page, total_pages)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=text,
                parse_mode='Markdown',
                reply_markup=keyboard
            )

        except Exception as e:
            print(f"Ошибка в show_other_files: {e}")
            bot.answer_callback_query(call.id, "❌ Произошла ошибка")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
    def handle_page_navigation(call):
        """Обработчик переключения страниц"""
        data = call.data.split('_')
        subject = data[1]
        type = data[2]
        page = int(data[3])

        subject_name = information_data.subjects_others[subject]
        type_name = information_data.file_types_others[type]

        # Получаем файлы из кэша
        cache_key = f"{subject}_{type}"
        if cache_key not in pagination_cache:
            bot.answer_callback_query(call.id, "❌ Данные устарели")
            return

        files = pagination_cache[cache_key]

        # Проверяем валидность страницы
        total_pages = (len(files) + information_data.FILES_PER_PAGE - 1) // information_data.FILES_PER_PAGE
        if page < 0 or page >= total_pages:
            bot.answer_callback_query(call.id, "❌ Неверная страница")
            return

        keyboard = create_files_keyboard(files, subject, type, page)
        text = get_page_text(files, subject_name, type_name, page, total_pages)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode='Markdown',
            reply_markup=keyboard
        )


    @bot.callback_query_handler(func=lambda call: call.data.startswith('oth_f_'))
    def send_other_file(call):
        """Отправить выбранный файл из other_files"""
        data = call.data.split('_')
        subject_key = data[2]
        type_key = data[3]
        file_index = int(data[4])

        cache_key = f"{subject_key}_{type_key}"
        if cache_key not in file_cache:
            bot.answer_callback_query(call.id, "❌ Данные устарели")
            return

        files = file_cache[cache_key]
        if file_index < 0 or file_index >= len(files):
            bot.answer_callback_query(call.id, "❌ Файл не найден")
            return

        filename = files[file_index]
        file_path = os.path.join(information_data.file_path_others, subject_key, type_key, filename)

        try:
            with open(file_path, 'rb') as file:
                bot.send_document(call.message.chat.id, file)
            bot.answer_callback_query(call.id, "Файл отправлен 📄")
        except:
            bot.answer_callback_query(call.id, "❌ Файл не найден")

    @bot.callback_query_handler(func=lambda call: call.data == 'back_to_allfiles_menu')
    def back_to_allfiles_menu(call):
        """Вернуться в главное меню allfiles"""
        all_mes(call.message)

    @bot.callback_query_handler(func=lambda call: call.data == 'find_by_subject')
    def back_to_find_subject(call):
        """Вернуться к выбору предмета"""
        find_by_subject(call)

    # Просмотр всех файлов
    @bot.callback_query_handler(func=lambda call: call.data == 'look_all_files')
    def look_all_files(call):
        files_found = False
        keyboard = types.InlineKeyboardMarkup()
        files = []
        for subject_key, subject_name in information_data.subjects_others.items():
            for typefolder in information_data.in_others_key:
                folder_path = os.path.join(information_data.file_path_others, subject_key, typefolder)
                # print(folder_path)
                if not os.path.exists(folder_path):
                    continue
                try:
                    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                except PermissionError:
                    continue

                if not files:
                    continue

                files_found = True
                for file in files:
                    # print(file)
                    keyboard.add(types.InlineKeyboardButton(text=f'{file}',
                                                            callback_data=f'others_'))  # Нужно продумать callback_data на примере работы с дз
        if not files_found:
            bot.send_message(call.message.chat.id, "📂 Файлы не найдены")
            return

        bot.send_message(call.message.chat.id, text='Вот все файлы, загруженные в систему ранее.',
                         parse_mode='MARKDOWN', reply_markup=keyboard)
