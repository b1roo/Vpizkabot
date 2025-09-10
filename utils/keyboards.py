from telebot import types
import information_data


def create_files_keyboard(files, subject, type, page=0):
    """Клавиатура для списка файлов с пагинацией"""
    keyboard = types.InlineKeyboardMarkup()

    # Вычисляем диапазон файлов для текущей страницы
    start_idx = page * information_data.FILES_PER_PAGE
    end_idx = start_idx + information_data.FILES_PER_PAGE
    page_files = files[start_idx:end_idx]

    # Добавляем файлы текущей страницы
    for i, file in enumerate(page_files):
        global_index = start_idx + i
        keyboard.add(types.InlineKeyboardButton(
            text=f"📄 {file}",
            callback_data=f"oth_f_{subject}_{type}_{global_index}"
        ))

    # Добавляем кнопки навигации если нужно
    row_buttons = []

    # Кнопка "Назад" если не первая страница
    if page > 0:
        row_buttons.append(types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data=f"page_{subject}_{type}_{page - 1}"
        ))

    # Кнопка "Добавить файл" всегда посередине
    row_buttons.append(types.InlineKeyboardButton(
        text=information_data.add_file_text,
        callback_data=f"add_{subject}_{type}"
    ))

    # Кнопка "Далее" если есть еще файлы
    if end_idx < len(files):
        row_buttons.append(types.InlineKeyboardButton(
            text="Далее ▶️",
            callback_data=f"page_{subject}_{type}_{page + 1}"
        ))

    keyboard.row(*row_buttons)

    # Кнопка "Назад к типам файлов"
    keyboard.add(types.InlineKeyboardButton(
        text=information_data.back_text,
        callback_data=f"oth_subj_{subject}"
    ))

    return keyboard


def create_homework_files_keyboard(files, subject, page=0):
    """Клавиатура для файлов домашних работ с пагинацией"""
    keyboard = types.InlineKeyboardMarkup()

    # Вычисляем диапазон файлов для текущей страницы
    start_idx = page * information_data.HOMEWORK_FILES_PER_PAGE
    end_idx = start_idx + information_data.HOMEWORK_FILES_PER_PAGE
    page_files = files[start_idx:end_idx]

    # Добавляем файлы текущей страницы
    for file in page_files:
        keyboard.add(types.InlineKeyboardButton(
            text=f"📄 {file}",
            callback_data=f"file_{subject}_{file}"
        ))

    # Добавляем кнопки навигации если нужно
    row_buttons = []

    # Кнопка "Назад" если не первая страница
    if page > 0:
        row_buttons.append(types.InlineKeyboardButton(
            text="◀️ Назад",
            callback_data=f"hwpage_{subject}_{page - 1}"
        ))

    # Кнопка "Далее" если есть еще файлы
    if end_idx < len(files):
        row_buttons.append(types.InlineKeyboardButton(
            text="Далее ▶️",
            callback_data=f"hwpage_{subject}_{page + 1}"
        ))

    if row_buttons:  # Добавляем строку навигации только если есть кнопки
        keyboard.row(*row_buttons)

    # Кнопка "Назад к предметам"
    keyboard.add(types.InlineKeyboardButton(
        text="◀️ Назад к предметам",
        callback_data="back_to_subjects"
    ))

    return keyboard


def get_page_text(files, subject_name, type_name, page, total_pages):
    """Генерируем текст для страницы"""
    start_idx = page * information_data.FILES_PER_PAGE
    end_idx = min(start_idx + information_data.FILES_PER_PAGE, len(files))

    text = f"📂 *{subject_name} - {type_name}*\n\n"

    if not files:
        text += "❌ Файлов не найдено\n\n📤 Вы можете добавить первый файл!"
    else:
        text += f"Файлы {start_idx + 1}-{end_idx} из {len(files)}\n"
        if total_pages > 1:
            text += f"Страница {page + 1} из {total_pages}\n\nВыберите файл:"
        else:
            text += "\nВыберите файл:"

    return text


def get_homework_page_text(files, subject_name, page, total_pages):
    """Генерируем текст для страницы домашних работ"""
    start_idx = page * information_data.HOMEWORK_FILES_PER_PAGE
    end_idx = min(start_idx + information_data.HOMEWORK_FILES_PER_PAGE, len(files))

    text = f"📂 *{subject_name}*\n\n"

    if not files:
        text += "❌ Файлов не найдено"
    else:
        text += f"Файлы {start_idx + 1}-{end_idx} из {len(files)}\n"
        if total_pages > 1:
            text += f"Страница {page + 1} из {total_pages}\n\nВыберите файл:"
        else:
            text += "\nВыберите файл:"

    return text
